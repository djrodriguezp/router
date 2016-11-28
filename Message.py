import re
class Message:
    def __init__(self, string):
        self.message = None
        self.text = string
        print "Parsing text: ", string
        if string.endswith("\n"):
            string = string.rstrip("\n")

        lines = string.split("\n")
        if len(lines) < 2:
            raise Exception("Message too short")

        header1 = lines.pop(0)
        headerMatch = re.match("^\s*From\s*:\s*(\w+)\s*$", header1)

        if headerMatch:
            self.origin = headerMatch.group(1);
        else:
            raise Exception("Invalid from header -> "+header1)

        header2 = lines.pop(0)
        headerMatch = re.match("^\s*(To|Type)\s*:\s*(\w+)\s*$", header2)

        if headerMatch:
            if headerMatch.group(1) == "Type":
                self.type = headerMatch.group(1);
                if re.match("^(?:HELLO|WELCOME|KeepAlive|DV)$", headerMatch.group(2)) is not None:
                    self.type = headerMatch.group(2)
                    if self.type == "DV":
                        if len(lines) > 0:
                            routesLenght = lines.pop(0)
                            headerMatch = re.match("^\s*Len\s*:\s*(\d+)\s*$", routesLenght)

                            if headerMatch:
                                if len(lines) == int(headerMatch.group(1)):
                                    for line in lines:
                                        if re.match("^\s*\w+\s*:\s*\d+\s*$", line) is None:
                                            raise Exception("Invalid route format -> "+line)
                                    self.message = list(lines)
                                else:
                                    raise Exception("Len header mismatch with the amount of routes received -> Len:"+headerMatch.group(1)+", routes received:" + str(len(lines)))
                            else:
                                raise Exception("Invalid header Len -> "+routesLenght)
                        else:
                            raise Exception("Invalid DV message, no routes found")
                else:
                    raise Exception("Invalid Type header -> "+headerMatch.group(2))
            else:
                self.type = "application"
                self.to = headerMatch.group(2)
                if len(lines) > 0:
                    headerMatch = re.match("^\s*Msg\s*:\s*(.*)$", lines[0])
                    #eliminamos la cabecera Msg y EOF
                    if headerMatch is not None:
                        lines[0] = headerMatch.group(1)
                        lastLine = lines.pop()
                        if re.match("^\s*EOF\s*$", lastLine):
                            self.message = list(lines)
                        else:
                            raise Exception("EOF not found in message")
                    else:
                        raise Exception("Invalid Msg header -> " + lines[0])
                else:
                    raise Exception("Invalid application message, no Msg found")
        else:
            raise Exception("Invalid header -> "+header2)
