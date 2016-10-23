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



