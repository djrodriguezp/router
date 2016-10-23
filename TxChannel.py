from NetChannel import NetChannel
from time import sleep
import Routing
import socket

class TxChannel(NetChannel):
    def __init__(self, name, messageSender, socket):
        NetChannel.__init__(self, name="TX-"+name)
        self.socket = socket
        self.messageSender = messageSender

    def run(self):
        self.messageSender.send(self.socket, "HELLO")
        self.socket.recv(4096)
        alive = True
        while alive:
            sleep(Routing.Routing.UPDATE_TIME_SEC)
            alive = self.messageSender.send(self.socket, "KeepAlive")
            if not alive:
                print self.name + " Dying :("

