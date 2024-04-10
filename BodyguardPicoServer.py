
import socket
import sys
import os
import time
import copy
import datetime as dt
import threading
import queue
#from threading import Thread, currentThread

portnumber = 10001
#portnumber = 12348
data1 = ""
#input_command = "BBBB"
command = ""
new_client_address = ""
new_clientsocket = ""
#localhost = socket.gethostname()
localhost = "192.168.20.104"
#localhost = "192.168.11.100"
#TERMINATION_CHAR = '/'
TERMINATION_CHAR = '\n'
# 将全局使用的变量定义在类中        
#ALIVE_FLAG = "alive"
class G:
    input_command = "GET STARTED.."+TERMINATION_CHAR
    new_input = True
    message_from_tower = " "
    lock = threading.Lock()
    message_received = False
    
    

class Server:
    """ socket 服务端 """
    #global input_command, new_input, lock
    
    def __init__(self,port,host= localhost):
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
        self._sock.bind((host, self.port))
        
        self.msg = None
        self.new_command = None
        self.new_message = None
        self.already_sent = False
        self.time_alive = time.time()
        self.ALIVE_FLAG = "ALIVE"+TERMINATION_CHAR
        
        print(f"the server IP is {host},{self.port}")
        """ 开启服务 """
        self._sock.listen(5)
        print("Serving...")
        print("Waiting for connection...")
        self.conn, self.addr = self._sock.accept()
        print(f"Recived new conn: {self.conn} from {self.addr}")
            

    def read(self, conn: socket.socket = None):
        """ 从tcp连接里面读取数据 """
        while True:
            try:
                data = self.conn.recv(1024).decode()
            except Exception as e:
                print("recv failed: %s", e)
                return
            print(f"[Received]-->>port of {self.port} and thread number is:", threading.current_thread().ident, data)
            #print("[R %s]<< %s", threading.current_thread().ident, data)
            #temp = data.split("/")
            temp = data.split()
            self.msg = temp[-1]
            
            if self.msg == "Photoeye:ON":
                G.message_from_tower = "Photoeye:ON"
            if self.msg == "Photoeye:OFF":
                G.message_from_tower = "Photoeye:OFF"
            
            
            G.lock.acquire()
            G.message_received = True
            G.lock.release()
            #time.sleep(1)

    def write(self, conn: socket.socket = None):
    	while True:
            msg = f"{dt.datetime.now()} - {self.msg}"
            #print("[W %s]>> %s", threading.current_thread().ident, msg)
            try:
                #conn.send(msg.encode())

                #input_command=q.get()
                #print(f"{G.input_command}command sent to tower")
                
                #if G.input_command != self.new_command: #and self.already_sent == False:
                if G.message_received == True:
                    G.lock.acquire()
                    G.message_received = False
                    G.lock.release()
                	#20240326ja
                	#conn.send(self.new_command.encode())
            
                if G.new_input == True:
                        G.lock.acquire()
                        G.new_input = False
                        self.new_command = G.input_command
                        G.lock.release()
                        self.conn.send(self.new_command.encode())
                        print(f"{self.new_command}command sent to Master")
                    #self.already_sent = True
                if G.message_from_tower != self.new_message : #and self.already_sent == False:
                    self.new_message = G.message_from_tower
                   
                    #if self.new_message == "Photoeye:ON":
                        #conn.send(bytes(f"/All_ON","utf-8"))
                        
                        #print("LED ON command sent to tower")
                    #if self.new_message == "Photoeye:OFF":
                        #conn.send(bytes(f"/All_OFF","utf-8"))
                       
                        #print("LED OFF command sent to tower")
                
                if time.time() - self.time_alive >= 4:
                    self.time_alive  = time.time()
                    self.conn.send(self.ALIVE_FLAG.encode())
                    print("ALIVE EVERY 4 SECOND")
                	
            #except :
            	#print("send failed: %s", e)
            	#pass
                
                    
            except Exception as e:
                print("send failed: %s", e)
            finally:
            	pass
                #return
            #time.sleep(1)
    
    def serve(self):
        """ 开启服务 """
        self._sock.listen(5)
        print("Serving...")
        while True:
            print("Waiting for connection...")
            conn, addr = self._sock.accept()
            print(f"Recived new conn: {conn} from {addr}")
            # 开启读写线程处理当前连接
            threading.Thread(target=self.read, daemon=True,args=(conn, )).start()
            threading.Thread(target=self.write, daemon=True,args=(conn, )).start()

def get_input():
    #global input_command
    #global q
    while True:
        try :
            G.input_command = input()
            G.input_command += TERMINATION_CHAR
            G.lock.acquire()
            G.new_input = True
            G.lock.release()
            
            #q.put(input_command)
            print(f"Key input is {G.input_command}")
            
        except EOFError as e:
            print(e)
        except KeyboardInterrupt:
            print("you press Ctrl + C")
        except:
            pass
            

if __name__ == '__main__':

    #q=queue.Queue(1) 
    #localhost = socket.gethostname()
    #lock = threading.lock()
    
    
    server_to_tower1 = Server(10001)
    #threading.Thread(target= server_to_tower1.serve , daemon=True).start()

    threading.Thread(target=server_to_tower1.read, daemon=True).start()
    threading.Thread(target=server_to_tower1.write, daemon=True).start()
    #server_to_tower2 = Server(10002)                                      
    #threading.Thread(target= server_to_tower2.serve , daemon=True).start()

    input_thread = threading.Thread(target=get_input, daemon=True).start()

   
    #s.serve()

    while True:
        try:
            time.sleep(20)
            print(f"main thread of {threading.get_ident()} is alive.....")
            print(f"the pid is {os.getpid()}")
        except KeyboardInterrupt:
            print("you just pressed control + C, and it exited")
            exit()
