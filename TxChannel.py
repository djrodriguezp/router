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
        self.messageSender.ownerName = self.name
        self.messageSender.send(self.socket, "HELLO")
        #TODO: check welcome
        print "Waiting for welcome..."
        self.socket.settimeout(None)
        data = self.socket.recv(4096)
        print "Welcome received:\n", data
        success = True
        while self.alive and success:
            sleep(Routing.Routing.INSTANCE.UPDATE_TIME_SEC)
            self.checkForNewShortestPath()
            success = self.alive and (self.sendUpdateIfNeeded() or self.messageSender.send(self.socket, "KeepAlive"))
        print self.name + " Dying :("

    def checkForNewShortestPath(self):
        if self.shortestPathProvider is not None:
            self.dvR2SR2Go = list(self.shortestPathProvider.getNewShortestPaths(self.name))
            print "these are the new paths for ", self.name, self.dvR2SR2Go

    def sendUpdateIfNeeded(self):
        if len(self.dvR2SR2Go) > 0:
            self.dvR2SR2Go = ["Len:"+str(len(self.dvR2SR2Go))] + self.dvR2SR2Go
            self.messageSender.send(self.socket, "DV", self.dvR2SR2Go)
            self.dvR2SR2Go = []
            return True
        return False
