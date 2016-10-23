from NetChannel import NetChannel
from time import sleep
import Routing
import socket

class TxChannel(NetChannel):

    shortestPathProvider = None

    def __init__(self, name, messageSender, socket):
        NetChannel.__init__(self, name="TX-"+name)
        self.socket = socket
        self.messageSender = messageSender
        self.alive = True
        self.dvR2SR2Go = []

    def die(self):
        self.alive = False
        

    def run(self):
        self.messageSender.send(self.socket, "HELLO")
        #TODO: check welcome
        self.socket.recv(4096)
        success = True
        while self.alive and success:
            sleep(Routing.Routing.UPDATE_TIME_SEC)
            self.checkForNewShortestPath()
            success = self.alive and (self.sendUpdateIfNeeded() or self.messageSender.send(self.socket, "KeepAlive"))
        print self.name + " Dying :("

    def checkForNewShortestPath(self):
        if self.shortestPathProvider is not None:
            self.dvR2SR2Go = self.shortestPathProvider.getNewShortestPaths()

    def sendUpdateIfNeeded(self):
        if len(self.dvR2SR2Go) > 0:
            self.messageSender.send(self.socket, "DV", self.dvR2SR2Go)
            self.dvR2SR2Go = None
            return True
        return False
