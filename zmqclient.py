# #client.py
# import zmq, time
# context = zmq.Context()
# socket = context.socket(zmq.REQ)
# socket.connect("tcp://localhost:15555")
# for request in range(10):
 
#     print("Sending request {} …".format(request))
#     socket.send(b"Hello")
#     # time.sleep(1)
#     # message = socket.recv()
# #     # print("Received reply {} [ {} ]". format(request, message))
# # socket.close()
# context.term()

# https://medium.com/@laurent.mendil/have-two-or-more-python-scripts-talk-together-a-look-into-asynchronous-messaging-zmq-fdb38ab4b29d


import socket
import os 
def client():
  host = socket.gethostname()  # get local machine name
  port = 18081  # Make sure it's within the > 1024 $$ <65535 range
  print(f"client host :{host}")
  s = socket.socket()

  print(f"socket = {s}")
  s.connect((host, port))
  print(f"the pid is {os.getpid()}")
  
  message = input('-> ')
  while message != 'q':
    s.send(message.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    print('Received from server: ' + data)
    message = input('==> ')
  s.close()

if __name__ == '__main__':
  client()