import zmq
context = zmq.Context()
socket = context.socket(zmq.REQ)
#socket.connect("tcp://127.0.0.1:5000")
socket.connect("tcp://192.168.1.35:5000")
#socket.connect("tcp://127.0.0.1:6000")

import sys
def rexec(socket, msg, isrecv=False):
    socket.send(msg)
    print "Sending", msg
    if isrecv:
        msg_in = socket.recv()
        return msg_in

for i in range(10):
    msg = "msg %s" % i
    socket.send(msg)
    print "Sending", msg
    msg_in = socket.recv()

while True:
    #print "> "
    #s = sys.stdin.readline()
    s = raw_input("> ")   # Python 2.x
    #s = input("> ")      # Python 3
    print "echo: " + s
    if s == "exit":
        rexec(socket, "exit")
        print "Exiting..."
        sys.exit()
    else:
        rexec(socket, s, True)

socket.send("exit")
