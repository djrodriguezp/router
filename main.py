from Routing import Routing
from Forwarding import Forwarding

def start():
    forwardingModule = Forwarding()
    routingModule = Routing()

    f = open("router.conf", "r")
    for line_no, line in enumerate(f):
        line = line.strip()
        if line.startswith("updateTimeSeconds:"):
            routingModule.UPDATE_TIME_SEC = int(line.split(":")[1])
        elif line.startswith("bindIp:"):
            routingModule.BIND_IP = line.split(":")[1]
        elif line.startswith("routerName:"):
            routingModule.SAY_MY_NAME = line.split(":")[1]
    routingModule.run()
    forwardingModule.run()

start()
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("192.168.2.153",9080))
MessageSender(say_my_name).send(s, "CUALQUIER", ["MIERDA 1", "MIERDA 2", "MIERDA 3"])
s.close()
"""


