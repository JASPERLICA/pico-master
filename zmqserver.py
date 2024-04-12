#server.py

# import time
# import zmq

# context = zmq.Context()
# socket = context.socket(zmq.REP)
# socket.bind("tcp://*:15555")
# while True:
#     message = socket.recv() # Wait for next request from client
#     print("Received request: {}".format(message))
#     # Do some ‘work’
#     time.sleep(1)
#     message = b"World"
#     socket.send(message) # Send reply back to client

# import os
# import time
# import zmq
# import threading

# # def command_from_web(socket_zmq):
# #         print("it is in the function")
# #         while True:
# #             message = socket_zmq.recv() # Wait for next request from client
# #             print("Received request: {}".format(message))
# #             print(f"zmq socket thread of {threading.get_ident()} is alive.....")
# #             print(f"the pid is {os.getpid()}")
# #             # Do some ‘work’
# #             # time.sleep(1)
# #             # message1 = f"server received {message}"
# #             # socket_zmq.send(message1.encode()) # Send reply back to client)
# #             #s.serve()


# if __name__ == '__main__':
    
#     context = zmq.Context()
#     socket_zmq = context.socket(zmq.REP)
#     socket_zmq.bind("tcp://*:15555")

#     # print(socket_zmq)
#     # input_thread = threading.Thread(target=command_from_web, args=(socket_zmq,), daemon=True).start()

#     while True:
#         try: 
            
#             print("start")
#             message = socket_zmq.recv() # Wait for next request from client
#             print("Received request: {}".format(message))
#             print(f"zmq socket thread of {threading.get_ident()} is alive.....")
#             print(f"the pid is {os.getpid()}")
#             time.sleep(1)
#             message = b"World"
#             socket_zmq.send(message) # Send reply back to client
#         except KeyboardInterrupt:
#             print("main thread exit")
#         except:
#             print("something wrong")
#             socket_zmq.close()
#             context.term()
#             exit()

import socket
import os
def server():
  host = socket.gethostname()   # get local machine name
  port = 18081  # Make sure it's within the > 1024 $$ <65535 range
  
  print(f"server host :{host}")
  s = socket.socket()
  s.bind((host, port))
  print(f"the server's pid is {os.getpid()}")
  s.listen(1)
  client_socket, address = s.accept()
  print(f"client_socket = {client_socket},address = {address}")
  print("Connection from: " + str(address))
  while True:
    data = client_socket.recv(1024).decode('utf-8')
    if not data:
      break
    print('From online user: ' + data)
    data = data.upper()
    client_socket.send(data.encode('utf-8'))
  client_socket.close()

if __name__ == '__main__':
    server()