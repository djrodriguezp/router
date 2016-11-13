import socket

class Logger:

    INSTANCE = None

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        Logger.INSTANCE = self

    def write(self, msg, lines = []):
        appendLines = lambda m,line: m + line + "\n"
        MESSAGE = reduce(appendLines, lines, msg)

        print msg + "\n"
        for l in lines:
            print l + "\n"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        s.send(MESSAGE)
        s.close()