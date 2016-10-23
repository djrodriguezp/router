# coding=utf-8
import socket

from MessageSender import MessageSender
from RoutingLobby import RoutingLobby
from TxChannel import TxChannel

class Path:
    changed = True
    cost = 99
    neighbor = None

    def __init__(self, neighbor, cost = 99):
        self.neighbor = neighbor
        self.cost = cost
        pass


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

    def getNewShortestPaths(self):
        pass

class DistanceVectorListener:

    def receivedDVMessage(self, dvmsg, origin):
        pass

class Routing(ShortestPathProvider, DistanceVectorListener):

    ROUTING_PORT = 9080
    say_my_name = "0xETSONHUECO"
    listenOnIp = "192.168.1.20"
    UPDATE_TIME_SEC = 10
    table = {}

    shortestPaths = {}

    def __init__(self):
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
                s.connect((node.ip, Routing.ROUTING_PORT))
            except Exception as e:
                print "No se pudo establecer conexión tcp con " + node.name + "(" + node.ip + ")"
                print(e)
            else:
                node.tx = TxChannel(node.name, MessageSender(Routing.say_my_name), s)
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

        RoutingLobby(self.listenOnIp, self.ROUTING_PORT, self).start()

        for node in filter(lambda x: x.tx is not None, self.neighbors):
            node.tx.dvR2SR2Go = self.getNewShortestPaths()
            node.tx.start()

    def getNewShortestPaths(self):
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
            if curr.changed:
                lines.append(to + ":" + str(curr.cost))
                curr.changed = False

        if len(lines) > 0:
            print "The following shortest paths changed: " , lines
        print "Current shortest paths", self.shortestPaths

        return lines

    def receivedDVMessage(self, dvmsg, origin):
        dvmsg = map(lambda x: x.split(":"), dvmsg)
        for line in dvmsg:
            to = line[0]
            cost = int(line[1])
            if to not in self.shortestPaths:
                self.shortestPaths[to] = Path(origin, 99)
            reportedCost = self.shortestPaths[origin].cost + cost
            if reportedCost < self.shortestPaths[to].cost:
                self.shortestPaths[to] = Path(origin, reportedCost)
        pass