from threading import *
import socket
class NetChannel(Thread):

    def __init__(self, name, ip=None, port = 9080):
        Thread.__init__(self, name=name)
        self.name = name
        self.ip = ip
        self.port = port

    def run(self):
        pass

