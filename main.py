from MessageSender import MessageSender
from TxChannel import TxChannel

def read_conf_file(filename):
    f = open(filename, "r")
    neighbors = []
    for line_no, line in enumerate(f):
        node_data = line.rstrip().split(";")
        if len(node_data) != 3:
            raise AssertionError("Expected 3 values delimited by ; at line " + str(line_no + 1) + " file: " + filename)
        #neighbors.append(Node(node_data[0], int(node_data[1]), node_data[2]))
    #return neighbors



say_my_name = "0xBEEFBABE"

msgs = MessageSender(say_my_name).sendHello(socket=None)


"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((node.ip,DEST_PORT))
    s.send("FROM" + say_my_name + "\n" + "TYPE:HELLO");
    s.close();
"""

