#client.py
import zmq
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:15555")
for request in range(10):
 
    print("Sending request {} …".format(request))
    socket.send(b"Hello")
    message = socket.recv()
    print("Received reply {} [ {} ]". format(request, message))
socket.close()
context.term()