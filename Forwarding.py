import socket
import select
from Message import Message
from threading import Thread
from Routing import Routing

class Forwarding(Thread):

    def __init__(self):
        super(Forwarding, self).__init__()
        self.port = 1981
        self.address = Routing.BIND_IP

    def fordwardMessage(self,neighborIP):
        pass

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.address, self.port))
        print "Running forwarding, listening on "+self.address+":"+self.port
        s.listen(1)

        while True:
            conn, addr = s.accept()
            ready = select.select([conn], [], [])
            if ready[0]:
                data = conn.recv(1024)
                try:
                    msg = Message(data)
                except Exception as e:
                    print "Malformed application message from ", addr
                    print e.message
                else:
                    if msg.type == "application":
                        if msg.to == Routing.SAY_MY_NAME:
                            print "mensaje para miguelito recibido :D"
                        else:
                            try:
                                route = Routing.shortestPaths[msg.to]
                            except Exception:
                                print "No route found to "+msg.to+" dropping message"
                            else:
                                print "Forwarding message to "+msg.to+" through "+route.neighbor.name+" ip "+route.neighbor.ip
                    else:
                        print "Message type "+msg.type+" received on port "+self.port+" from ", addr , " dropping message "
                conn.close()

