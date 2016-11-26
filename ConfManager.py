import socket
import select
from threading import Thread
from Routing import Routing
from Logger import Logger


class ConfManager(Thread):

    def __init__(self, ip, port):
        super(ConfManager, self).__init__()
        self.ip = ip
        self.port = port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        print "Configuration Manager, listening on " + self.ip + ":" + str(self.port)
        s.listen(1)

        while True:
            conn, addr = s.accept()
            ready = select.select([conn], [], [])
            if ready[0]:
                data = conn.recv(1024)
                message = ""
                if data.startswith("GetConf"):
                    message = str(Routing.INSTANCE.UPDATE_TIME_SEC)+"|"+str(Routing.INSTANCE.TIMEOUT)+"|"
                    message += self.getNeighbors()
                    Logger.INSTANCE.write(Logger.NEIGHBORS, self.getNeighbors().split(";"))
                if data.startswith("SaveConf"):
                    try:
                        data = data.rstrip("\n")
                        confValues = data.split("|")
                        Routing.INSTANCE.UPDATE_TIME_SEC = int(confValues[1])
                        Routing.INSTANCE.TIMEOUT = int(confValues[2])
                        message = "OK"
                    except Exception as e:
                        message = "ERROR "+e.message
                if data.startswith("AddNode"):
                    try:
                        data = data.rstrip("\n")
                        nodeData = data.split("|")
                        nodeData.pop(0)

                        for neighbor in Routing.INSTANCE.neighbors:
                            if neighbor.name == nodeData[0]:
                                raise Exception("el vecino "+nodeData[0]+" ya se encuentra agregado como vecino")
                            if neighbor.ip == nodeData[2]:
                                raise Exception("la IP "+nodeData[2]+" ya se encuentra agregada como vecino")

                        node = Routing.INSTANCE.makeNode(nodeData)
                        if Routing.INSTANCE.connectNode(node):
                            message = "OK"
                        else:
                            message = "No ha sido posible conectarse con el nuevo vecino"
                    except Exception as e:
                        message = "ERROR "+e.message
                if data.startswith("RemoveNode"):
                    try:
                        data = data.rstrip("\n")
                        nodeData = data.split("|")
                        neighbor = Routing.INSTANCE.findNeighbor(nodeData[1])
                        if neighbor is not None:
                            if neighbor.tx is not None:
                                neighbor.tx.die()
                            if neighbor.rx is not None:
                                neighbor.rx.die()
                            message = "OK"
                        else:
                            message = "vecino no encontrado"
                    except Exception as e:
                        message = +e.message
                message += "\n"
                conn.send(message)
                conn.close()

    def getNeighbors(self):
        nList = ""
        for neighbor in Routing.INSTANCE.neighbors:
            nList += neighbor.name + ":" + neighbor.ip + ":"+str(neighbor.cost)+";"

        return nList

