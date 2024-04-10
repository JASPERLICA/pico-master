#server.py
import time
import zmq
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:15555")
while True:
    message = socket.recv() # Wait for next request from client
    print("Received request: {}".format(message))
    # Do some ‘work’
    time.sleep(1)
    message = b"World"
    socket.send(message) # Send reply back to client