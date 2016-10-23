# coding=utf-8
import socket

from MessageSender import MessageSender
from TxChannel import TxChannel
ROUTING_PORT = 9080
say_my_name = "0xBEEFBABE"

def read_conf_file(filename):
    f = open(filename, "r")
    for line_no, line in enumerate(f):
        node = line.rstrip().split(";")
        if len(node) != 3:
            raise AssertionError("Expected 3 values delimited by ; at line " + str(line_no + 1) + " file: " + filename)
        name = node[0]
        ip = node[2]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, ROUTING_PORT))
        except Exception as e:
            print "No se pudo establecer conexión tcp con " + name + "(" + ip + ")"
            print(e)
        else:
            TxChannel(name, MessageSender(say_my_name), s).start()



#read_conf_file("neighbors.conf")



names = ["a", "b", "c"]



"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("192.168.2.153",9080))
MessageSender(say_my_name).send(s, "CUALQUIER", ["MIERDA 1", "MIERDA 2", "MIERDA 3"])
s.close()
"""


