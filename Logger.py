import socket

class Logger:

    INSTANCE = None
    DV = "DV"
    PATHS = "SP"
    NEIGHBORS = "N"

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        Logger.INSTANCE = self

    def write(self, msg, lines = []):
        appendLines = lambda m,line: m + line + "\n"
        MESSAGE = reduce(appendLines, lines, msg + "\n")

        print msg + "\n"
        for l in lines:
            print l + "\n"

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
            s.send(MESSAGE)
            s.close()
        except Exception as e:
            print e
