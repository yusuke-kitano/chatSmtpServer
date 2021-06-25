import smtpd
from requests.api import head
import chatwork
import base64
import smtplib
from email.mime.text import MIMEText
import quopri

# クラス：チャットSMTPクラス
class ChatSMTPServer(smtpd.SMTPServer):
    config = {}
    
    def __init__(self, localaddr, remoteaddr, data_size_limit: int, map, enable_SMTPUTF8: bool, decode_data: bool,config) :
        super().__init__(localaddr, remoteaddr, data_size_limit=data_size_limit, map=map, enable_SMTPUTF8=enable_SMTPUTF8, decode_data=decode_data)
        self.config = config

    # SMTP受信処理
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        print(peer)
        print(mailfrom)
        print(rcpttos)

        # コンテンツの取得
        (subject, content) = self.get_contents(data)

        # chat送信
        self.chat_send(rcpttos, subject, content)

        # mail送信
        self.mail_send(mailfrom, rcpttos, subject, content)

        return

    # メッセージコンテンツ取得
    def get_contents(self, data):
        # コンテンツの解析
        headers = {}
        rows = data.split('\n')
        contentRow = 0
        for index,row in enumerate(rows):
            if row.strip() == "":
                contentRow = index    
                break
            if len(row.split(':')) == 2:
                [key, value] = row.split(':')
                headers[key] = value.strip()    

        subject = ""
        content = ""
        # 件名の解析
        if len(headers["Subject"].split("?")) > 3:
            transferEncoding = headers["Subject"].split("?")[2]
            if transferEncoding == "B":
                subjectBase64 = headers["Subject"]
                subject = base64.b64decode(subjectBase64.split("?")[3]).decode()
            if transferEncoding == "Q":
                subjectBase64 = headers["Subject"]
                subject = quopri.decodestring(subjectBase64.split("?")[3]).decode()
        else:
            subject = headers["Subject"]

        # 本文の解析
        contents = rows[contentRow:]
        if headers["Content-Transfer-Encoding"] == "base64":
            # base64
            for b64Content in contents:
                content += base64.b64decode(b64Content).decode() + "\n"
        elif headers["Content-Transfer-Encoding"] == "quoted-printable":
            #quoted-printable
            for qpContent in contents:
                content += quopri.decodestring(qpContent,header=False).decode() + "\n"
        else:        
            #平文
            content = "\n".join(rows[contentRow:])

        return (subject, content)

    # チャット送信メソッド
    def chat_send(self, rcpttos, subject, content):
        # 送信先判定＆送信処理
        sendto = set(self.config['toAddr'].split(","))
        sendtoAll = set(self.config['toAllAddr'].split(","))
        mailTo = set(rcpttos)
        intersectionTo = sendto & mailTo
        intersectionToAll = sendtoAll & mailTo
        if len(intersectionTo) > 0:
            cilent = chatwork.client(self.config['apiKey'])
            cilent.send(self.config['roomId'], subject, content)

        if len(intersectionToAll) > 0:
            cilent = chatwork.client(self.config['apiKey'])
            cilent.sendAll(self.config['roomId'], subject, content)

    # メールリレーメソッド
    def mail_send(self,  mailfrom, rcpttos, subject, content):
        msg = MIMEText(content)
        msg["To"] = ','.join(rcpttos)
        msg["From"] = mailfrom
        msg["Subject"] = subject
        # ローカルのメールサーバに投げる
        smtp = smtplib.SMTP(self.config['remoteHost'], int(self.config['remotePort']))
        smtp.sendmail(mailfrom, rcpttos, msg.as_string())
        smtp.quit()
