import socket
import select
from Message import Message
from threading import Thread
from Routing import Routing

class Forwarding(Thread):

    def __init__(self):
        super(Forwarding, self).__init__()
        self.port = 1981
        self.address = Routing.INSTANCE.BIND_IP

    def fordwardMessage(self,neighborIP,data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((neighborIP, self.port))
            s.send(data)
        except Exception as e:
            print "Error forwardeando"
        s.close()

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.address, self.port))
        print "Running forwarding, listening on "+self.address+":"+str(self.port)
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
                        if msg.to == Routing.INSTANCE.SAY_MY_NAME:
                            print "mensaje para miguelito recibido :D"
                        else:
                            try:
                                path = Routing.INSTANCE.shortestPaths[msg.to]
                            except Exception:
                                print "No route found to "+msg.to+" dropping message"
                            else:
                                destIP = Routing.INSTANCE.findNeighbor(path.neighbor).ip
                                print "Forwarding message to "+msg.to+" through "+destIP+" ip "
                                self.fordwardMessage(destIP, data)
                    else:
                        print "Message type "+msg.type+" received on port "+self.port+" from ", addr , " dropping message "
                conn.close()

