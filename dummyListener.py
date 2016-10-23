import socket
import select
import sys

TCP_IP = sys.argv[1]
TCP_PORT = 9080
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    ready = select.select([conn], [], [])
    if ready[0]:
        data = conn.recv(BUFFER_SIZE)
        print "received data:", data
        conn.send("WELCOME")


conn.close()