#--------------------------------------------------------------------
import signal
import sys
def signal_handler(signal, frame):
    global s, ser
    print '\nYou pressed Ctrl+C!'
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
#--------------------------------------------------------------------

import zmq
context = zmq.Context()
socket = context.socket(zmq.REP)
#socket.bind("tcp://127.0.0.1:5000")
socket.bind("tcp://192.168.1.35:5000")

while True:
    msg = socket.recv()
    if msg == "exit":
        print "Exiting..."
        sys.exit()
    print "Got", msg
    socket.send(msg)
