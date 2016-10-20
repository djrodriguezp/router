from NetChannel import NetChannel
import socket

class TxChannel(NetChannel):
    def __init__(self, name, messageSender):
        NetChannel.__init__(self, name="TX-"+name)
        self.messageSender = messageSender

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        self.messageSender.sendHello(s)
