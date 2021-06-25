from chatSMTPServer import ChatSMTPServer
import lib
import asyncore

if __name__ == "__main__":
    try:
        #設定ファイル読み込み
        iniData = lib.get_property('./server.property', 'utf-8')
        localServer = (iniData['localHost'], int(iniData['localPort']))
        server = ChatSMTPServer(localServer, None, data_size_limit=33554432,
                                map=None, enable_SMTPUTF8=False, decode_data=True,config=iniData)
        print("run!")
        print(localServer)
        asyncore.loop()
    except Exception as e :
        print(e)
        pass