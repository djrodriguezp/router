class MessageSender:
    def __init__(self, origin):
        self.origin = origin

    def send(self, socket, type, body = None):
        headers = self.makeHeaders(type)
        self.__send(socket, headers, body)

    def __send(self, socket, headers, body = None):
        if body is None:
            body = []
        appendHeader = lambda msg, head: msg + head[0] + ":" + head[1] + "\n"
        appendBody   = lambda msg, line: msg + line + "\n"

        message = reduce(appendHeader, headers, "")
        message = reduce(appendBody, body, message)

        print message
        try:
            socket.send(message)
        except:
            print "Error :3"

    def makeHeaders(self, type):
        return [ ("From", self.origin), ("Type", type) ]