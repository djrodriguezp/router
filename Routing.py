# coding=utf-8
import socket
import threading

from Logger import Logger
from MessageSender import MessageSender
from RoutingLobby import RoutingLobby
from TxChannel import TxChannel

class Path:
    def __init__(self, neighbor, cost = 99):
        self.neighbor = neighbor
        self.cost = cost
        self.alreadySent = []
        pass

    def shouldSendUpdate(self, txName):
        if txName not in self.alreadySent:
            self.alreadySent.append(txName)
            return True
        return False


class Node:
    def __init__(self, name, cost, ip):
        self.name = name
        self.cost = int(cost)
        self.ip = ip
        self.tx = None

class ShortestPathProvider:

    def getNewShortestPaths(self, txName):
        pass

class DistanceVectorListener:

    def receivedDVMessage(self, dvmsg, origin):
        pass

class Routing(ShortestPathProvider, DistanceVectorListener):

    ROUTING_PORT = 9080
    SAY_MY_NAME = "NONAME"
    BIND_IP = "127.0.0.1"
    UPDATE_TIME_SEC = 30
    TIMEOUT = 90
    table = {}

    INSTANCE = None

    shortestPaths = {}

    def __init__(self):
        Routing.INSTANCE = self
        self.neighbors = []
        self.tableLock = threading.RLock()

    def makeNode(self, nodeData):
        return Node(nodeData[0],nodeData[1],nodeData[2])

    def createDistanceMap(self):
        neighborsDict = {}
        for node in self.neighbors:
            neighborsDict[node.name] = 99
        return neighborsDict

    def read_conf_file(self, filename):
        f = open(filename, "r")
        for line_no, line in enumerate(f):
            nodeData = line.rstrip().split(";")
            if len(nodeData) != 3:
                raise AssertionError("Expected 3 values delimited by ; at line " + str(line_no + 1) + " file: " + filename)
            node = self.makeNode(nodeData)
            self.connectNode(node)

    def connectNode(self, node):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            Logger.INSTANCE.write("Trying to connect to " + node.ip + " " + node.name)
            s.settimeout(2)
            s.connect((node.ip, Routing.INSTANCE.ROUTING_PORT))
        except Exception as e:
            print "No se pudo establecer conexión tcp con " + node.name + "(" + node.ip + ")"
            print(e)
            return False
        else:
            print "Connected"
            self.addNeighbor(node, s, True)
            return True

    def initTable(self):
        for n in self.neighbors:
            self.updateTableNode(n)

    def updateTableNode(self, n):
        with self.tableLock:
            dmap = self.createDistanceMap()
            dmap[n.name] = n.cost
            self.table[n.name] = dmap
            self.shortestPaths[n.name] = Path(n.name, n.cost)

    def run(self):
        RoutingLobby(self.BIND_IP, self.ROUTING_PORT, self).start()
        self.read_conf_file("neighbors.conf")
        self.initTable()
        print self.table

        for node in filter(lambda x: x.tx is not None, self.neighbors):
            node.tx.start()

    def getNewShortestPaths(self, txName):
        with self.tableLock:
            #find the shortest path for every known node
            for to in self.table:
                min = self.shortestPaths[to].cost
                for neighbor in self.table[to]:
                    curr = self.table[to][neighbor]
                    if curr < min:
                        self.shortestPaths[to] = Path(neighbor, curr)
                        min = curr
            #serialize shortest paths with the 'changed' flag set
            lines = []
            for to in self.shortestPaths:
                curr = self.shortestPaths[to]
                if curr.shouldSendUpdate(txName):
                    lines.append(to + ":" + str(curr.cost))

            self.printShortestPaths()

            return lines

    def receivedDVMessage(self, dvmsg, origin):
        with self.tableLock:
            dvmsg = map(lambda x: x.split(":"), dvmsg)
            for line in dvmsg:
                to = line[0]
                cost = int(line[1])

                #ARREGLAR CUANDO TE MANDAN TU PROPIO NOMBRE
                reportedCost = 99
                if to == self.SAY_MY_NAME and self.findNeighbor(origin) is not None:
                    reportedCost = cost
                else:
                    reportedCost = self.shortestPaths[origin].cost + cost

                if to not in self.shortestPaths and to != self.SAY_MY_NAME:
                    dmap = self.createDistanceMap()
                    dmap[origin] = reportedCost
                    self.table[to] = dmap
                    self.shortestPaths[to] = Path(origin, reportedCost)
                elif to == self.SAY_MY_NAME:
                    if cost < self.shortestPaths[origin].cost:
                        self.shortestPaths[origin] = Path(origin, cost)
                    self.table[origin][origin] = cost
                elif reportedCost < self.shortestPaths[to].cost:
                    self.shortestPaths[to] = Path(origin, reportedCost)

    def findNeighbor(self, name):
        with self.tableLock:
            for neighbor in self.neighbors:
                if neighbor.name == name:
                    return neighbor
            return None

    def printShortestPaths(self):
        print "Current shortest paths"
        lines = []
        for to in self.shortestPaths:
            path = self.shortestPaths[to]
            msg = "to: " + to + "; via: " + path.neighbor + "; cost: " + str(path.cost)
            lines.append(msg)
            print msg

        Logger.INSTANCE.write(Logger.PATHS, lines)

    def addNeighbor(self, node, socket, isFromConfig):
        with self.tableLock:
            self.neighbors.append(node)
            node.tx = TxChannel(node.name, MessageSender(Routing.INSTANCE.SAY_MY_NAME), socket)
            node.tx.shortestPathProvider = self

            for to in self.table:
                self.table[to][node.name] = 99

            if not isFromConfig:
                self.updateTableNode(node)

