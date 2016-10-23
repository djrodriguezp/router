from NetChannel import NetChannel
from Routing import Routing
import select

class RxChannel(NetChannel):
    def __init__(self, name, messageSender, socket):
        NetChannel.__init__(self, name = "RX-" + name)
        self.socket = socket
        self.messageSender = messageSender


    def run(self):
        while True:
            ready = select.select([self.socket], [], [], Routing.UPDATE_TIME_SEC * 3)
            if ready[0]:
                data = self.socket.recv()
