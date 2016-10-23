import socket
import select
import Routing
from RxChannel import RxChannel
from threading import Thread
from Message import Message
from MessageSender import MessageSender
from TxChannel import TxChannel


class RoutingLobby(Thread):

    def __init__(self, address, port, dvListener):
        super(RoutingLobby, self).__init__()
        self.port = port
        self.address = address
        self.dvListener = dvListener

    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.address, self.port))
        print "Running routing lobby, listening on " + self.address + ":" + str(self.port)
        s.listen(1)

        alive = True
        while alive:
            conn, addr = s.accept()
            print "Started lobby connection with ", addr
            ready = select.select([conn], [], [])
            if ready[0]:
                data = conn.recv(1024)
                msg = None
                try:
                    msg = Message(data)
                except Exception as e:
                    print "Malformed HELLO message from ", addr
                    print e.message
                else:
                    print 'Accepted HELLO from: ', addr
                    RxChannel(msg.origin, MessageSender(Routing.Routing.INSTANCE.SAY_MY_NAME), conn, self.dvListener).start()
                    neighbor = Routing.Routing.INSTANCE.findNeighbor(msg.origin)
                    if neighbor is None:
                        pass #TODO: add neighbor
                    elif neighbor.tx is None:
                        newSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        newSock.settimeout(2)
                        newSock.connect((neighbor.ip, Routing.Routing.INSTANCE.ROUTING_PORT))
                        neighbor.tx = TxChannel(neighbor.name, MessageSender(Routing.Routing.INSTANCE.SAY_MY_NAME), newSock)
                        neighbor.tx.shortestPathProvider = Routing.Routing.INSTANCE
                        neighbor.tx.start()
