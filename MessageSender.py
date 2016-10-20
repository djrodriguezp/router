class MessageSender:
    def __init__(self, origin):
        self.origin = origin

    def sendHello(self, socket):
        headers = self.makeHeaders("HELLO")
        self.send(headers, socket)

    def send(self, headers,socket, body = None):
        if body is None:
            body = []
        message = reduce((lambda msg, head: msg + head[0] + ":" + head[1] + "\n"), headers, "")
        message = reduce((lambda msg, line: msg + line + "\n"), body, message)

        print message
        pass

    def makeHeaders(self, type):
        return [ ("From", self.origin), ("Type", type) ]