from Routing import Routing
from Forwarding import Forwarding

def start():
    Routing().run()
    Forwarding().run()

start()
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("192.168.2.153",9080))
MessageSender(say_my_name).send(s, "CUALQUIER", ["MIERDA 1", "MIERDA 2", "MIERDA 3"])
s.close()
"""


