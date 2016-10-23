# coding=utf-8
import socket

from MessageSender import MessageSender
from TxChannel import TxChannel

class Node:
    tx = None
    name = None
    cost = None
    ip = None

    def __init__(self, name, cost, ip):
        self.name = name
        self.cost = cost
        self.ip = ip

class Routing:

    ROUTING_PORT = 9080
    say_my_name = "0xBEEFBABE"
    UPDATE_TIME_SEC = 3
    table = {}

    def __init__(self):
        self.neighbors = []

    def makeNode(self, nodeData):
        return Node(nodeData[0],nodeData[1],nodeData[2])

    def createDistanceMap(self):
        neighborsDict = {}
        for node in self.neighbors:
            neighborsDict[node.name] = 99
        return neighborsDict

    def addNode(self, node):
        #self.nodes[node.name] = node.
        pass

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


        print 'sexo'


    def listen(self):
        pass

    def initTable(self):
        for n in self.neighbors:
            dmap = self.createDistanceMap()
            dmap[n.name] = n.cost
            self.table[n.name] = dmap

    def run(self):
        self.read_conf_file("neighbors.conf")
        self.initTable()
        print self.table
        startNode = lambda node: node.tx.start()
        map(startNode, filter(lambda x: x.tx is not None, self.neighbors))