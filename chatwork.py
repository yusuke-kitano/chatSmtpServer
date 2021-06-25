import requests

# チャットワーククライアントクラス


class client(object):
    URL = 'https://api.chatwork.com/v2'
    MESSAGES_URL = URL + "/rooms/{0}/messages"
    MEMBERS_URL = URL + "/rooms/{0}/members"
    TASKLIST_URL = URL + "/rooms/{0}/tasks"
    TASK_URL = URL + "/rooms/{0}/tasks/{1}"
    APIKEY = ''
    headers = {}

    def __init__(self, APIKEY):
        self.APIKEY = APIKEY
        self.headers = {'X-ChatWorkToken': self.APIKEY}

    # 送信内容を作成する(内容,タイトル,全員送信[0:Off,1:On],宛先[Option] )
    def __makeBody(self, content, title="", toAll=0, sendList=[]):
        body = ""
        if toAll == 1:
            body = "[toall]\n"
        else:
            for sendTo in sendList:
                body += "[To:{0}] {1}さん \n".format(sendTo["account_id"],
                                                   sendTo["name"])

        if title.strip() == "":
            body += content
        else:
            body += "[info][title]" + title + "[/title]" + content + "[/info]"
        return body

    # メッセージを送る
    def send(self, roomId, title, content):
        url = self.MESSAGES_URL.format(roomId)
        params = {'body': self.__makeBody(content, title)}
        resp = requests.post(url, headers=self.headers, params=params)

        print(resp.content)

    # 全員に送る
    def sendAll(self, roomId, title, content):
        url = self.MESSAGES_URL.format(roomId)
        params = {'body': self.__makeBody(content, title, 1)}
        resp = requests.post(url, headers=self.headers, params=params)

        print(resp.content)

    # 特定のIDに送る
    def sendTo(self, roomId, title, content, sendList):
        url = self.MESSAGES_URL.format(roomId)
        params = {'body': self.__makeBody(content, title, 0, sendList)}
        resp = requests.post(url, headers=self.headers, params=params)

        print(resp.content)

    # 最新メッセージを取得（最大100件）
    def getMessages(self, roomId, limit=100):
        url = self.MESSAGES_URL.format(roomId)
        params = {'force': '1'}
        resp = requests.get(url, headers=self.headers, params=params)
        # 取得したメッセージを返却
        if resp.content:
            datas = resp.json()
        else:
            datas = []
        return datas[-limit:]

    # 未読メッセージを取得
    def getUnReadMessages(self, roomId):
        url = self.MESSAGES_URL.format(roomId)
        params = {'force': '0'}
        resp = requests.get(url, headers=self.headers, params=params)
        # 取得したメッセージを返却
        if resp.content:
            datas = resp.json()
        else:
            datas = []
        return datas

    # 未完了タスクリストを取得（最大100件）
    def getTaskList(self, roomId, limit=100):
        url = self.TASKLIST_URL.format(roomId)
        params = {"status": "open"}
        resp = requests.get(url, headers=self.headers, params=params)
        # 取得したタスクを返却
        if resp.content:
            datas = resp.json()
        else:
            datas = []
        return datas[-limit:]

    # 完了タスクリストを取得（最大100件）
    def getDoneTaskList(self, roomId, limit=100):
        url = self.TASKLIST_URL.format(roomId)
        params = {"status": "done"}
        resp = requests.get(url, headers=self.headers, params=params)
        # 取得したタスクを返却
        if resp.content:
            datas = resp.json()
        else:
            datas = []
        return datas[-limit:]

    # タスク完了
    def doneTask(self, roomId, task_id):
        url = self.TASK_URL.format(roomId, task_id) + "/status"
        params = {"body": "done"}
        resp = requests.put(url, headers=self.headers, params=params)
        print(resp.content)

    pass
