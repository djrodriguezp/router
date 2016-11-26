import socket
import select
from threading import Thread

class ConfManager(Thread):

    def __init__(self, ip, port):
        super(ConfManager, self).__init__()
        self.ip = ip
        self.port = port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        print "Configuration Manager, listening on " + self.ip + ":" + str(self.port)
        s.listen(1)

        while True:
            conn, addr = s.accept()
            ready = select.select([conn], [], [])
            if ready[0]:
                data = conn.recv(1024)
                print "received conf command"
                if data.startswith("GetConf"):
                    conn.send("10|30|A,B,C,D\n")
                conn.close()