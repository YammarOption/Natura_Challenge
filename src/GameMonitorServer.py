from PyQt5.QtCore import QThread
import socket
import configparser



class GameMonitorServer(QThread):
    def __init__(self,mainWindowSignal,config:configparser.ConfigParser):
        super().__init__()
        self.mainWindowSignal=mainWindowSignal
        self.host="127.0.0.1"
        self.port=config.getint("MAIN","port")
        self.timeout=config.getint("MAIN","timeout")

    def close(self):
        if self.conn:
             self.conn.close()

    def run(self):
        self.conn=None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host,self.port))
        self.socket.listen
        self.socket.settimeout(self.timeout)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.listen()
        while True:
            try: 
                print("server waiting")
                self.conn,self.addr = self.socket.accept()
                with self.conn:
                        print("server connected")
                        while True:
                            data = self.conn.recv(1024)
                            if not data: break
                            strData=data.decode('utf-8')
                            self.mainWindowSignal.emit("GAMELOG",strData)
            except Exception as e:
                 print(e)
                        
