import socket
import sys
dest_ip = sys.argv[1]
destPort = 9080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((dest_ip, destPort))
print 'Connected, ready to send messages:'
while True:
    lines = []
    line = ""
    print ">"
    while line != ":s":
        line = raw_input("")
        if line != ":s":
            lines.append(line.replace('>', ''))

    appendBody = lambda msg, line: msg + line + "\n"
    message = reduce(appendBody, lines, "")
    try:
        s.send(message)
    except Exception as e:
        print e
    else:
        print "sent\n" , message
