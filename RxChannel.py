from Message import Message
from NetChannel import NetChannel
import Routing
import select

class RxChannel(NetChannel):
    def __init__(self, name, messageSender, socket, dvListener):
        NetChannel.__init__(self, name = "RX-" + name)
        self.socket = socket
        self.messageSender = messageSender
        self.dvListener = dvListener


    def run(self):
        self.messageSender.ownerName = self.name
        self.messageSender.send(self.socket, "WELCOME")
        while True:
            ready = select.select([self.socket], [], [], Routing.Routing.INSTANCE.TIMEOUT)
            if ready[0]:
                data = self.socket.recv(1024)
                try:
                    msg = Message(data)
                except Exception as e:
                    print "Malformed DV or KeepAlive message from ", self.name
                    print e.message
                    if data == "":
                        print "Dying because of empty message"
                        break

                else:
                    print "received " + msg.type + " message from " + msg.origin
                    print msg.message
                    if msg.type == "DV":
                        self.dvListener.receivedDVMessage(msg.message, msg.origin)
            else:
                print "Timeout"
                break
        print self.name + " dying :("