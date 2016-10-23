class Message:
    def __init__(self, string):
        lines = string.split("\n")
        fromHeader = lines[0].split(":")
        if len(fromHeader) != 2:
            pass

