# coding=utf-8
import socket

from MessageSender import MessageSender
from RoutingLobby import RoutingLobby
from TxChannel import TxChannel

class Path:
    changed = True
    cost = 99
    neighbor = None
    alreadySent = []

    def __init__(self, neighbor, cost = 99):
        self.neighbor = neighbor
        self.cost = cost
        pass

    def shouldSendUpdate(self, txName):
        if txName not in self.alreadySent:
            self.alreadySent.append(txName)
            return True
        return False


class Node:
    tx = None
    name = None
    cost = None
    ip = None

    def __init__(self, name, cost, ip):
        self.name = name
        self.cost = int(cost)
        self.ip = ip

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
    table = {}

    INSTANCE = None

    shortestPaths = {}

    def __init__(self):
        Routing.INSTANCE = self
        self.neighbors = []

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
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.neighbors.append(node)
            try:
                s.connect((node.ip, Routing.INSTANCE.ROUTING_PORT))
            except Exception as e:
                print "No se pudo establecer conexión tcp con " + node.name + "(" + node.ip + ")"
                print(e)
            else:
                node.tx = TxChannel(node.name, MessageSender(Routing.INSTANCE.SAY_MY_NAME), s)
                node.tx.shortestPathProvider = self

    def initTable(self):
        for n in self.neighbors:
            dmap = self.createDistanceMap()
            dmap[n.name] = n.cost
            self.table[n.name] = dmap
            self.shortestPaths[n.name] = Path(n.name, n.cost)

    def run(self):
        self.read_conf_file("neighbors.conf")
        self.initTable()
        print self.table

        RoutingLobby(self.BIND_IP, self.ROUTING_PORT, self).start()

        for node in filter(lambda x: x.tx is not None, self.neighbors):
            node.tx.start()

    def getNewShortestPaths(self, txName):
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

        if len(lines) > 0:
            print "The following shortest paths changed: " , lines
        print "Current shortest paths", self.shortestPaths

        return lines

    def receivedDVMessage(self, dvmsg, origin):
        dvmsg = map(lambda x: x.split(":"), dvmsg)
        for line in dvmsg:
            to = line[0]
            cost = int(line[1])
            reportedCost = self.shortestPaths[origin].cost + cost
            if to not in self.shortestPaths and to != self.SAY_MY_NAME:
                dmap = self.createDistanceMap()
                dmap[origin] = reportedCost
                self.table[to] = dmap
                self.shortestPaths[to] = Path(origin, reportedCost)
            elif to == self.SAY_MY_NAME:
                self.table[origin] = cost
