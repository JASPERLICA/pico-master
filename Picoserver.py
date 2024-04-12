import socket
import sys
import os
import time
import copy
import datetime as dt
import threading
import queue

master_port = 10001
web_port = 18001
TERMINATION_CHAR = '\n'
ALIVE_FLAG = "ALIVE"+TERMINATION_CHAR
class G:

    master_pool=[]
    web_pool=[]

    lock_master_message = threading.Lock()
    message_received_from_m = False
    message_from_master = " "
    
    buff_for_master = " "

    lock_web_message = threading.Lock()
    message_receiced_from_web = False
    message_from_web = " "

    buff_for_web = " "

    time_alive = time.time()

def master_message_handle(master_socket):

    while True:

        print(f"the master message handle pid is {os.getpid()}")
        try:
            data = master_socket.recv(1024).decode()
        except Exception as e:
            print(f"recv from master failed:{e}")
            return
        print(f"[Received from master data]-->>{data}-->> {threading.current_thread().ident}")

        temp = data.split()
        msg = temp[-1]
        
        
        G.lock_master_message.acquire()
        G.message_receiced_from_master = True

        if msg == "Photoeye:ON":
            G.message_from_master = "Photoeye:ON"
            pass
        if msg == "Photoeye:OFF":
            G.message_from_master = "Photoeye:OFF"
            pass

        G.lock_master_message.release()

        
        
def send_to_master(master_socket, message=""):

    message = message + TERMINATION_CHAR
    master_socket.send(message.encode())


def accept_master(to_master_sock: socket.socket):

    while True:
        print(f"the master accept pid is {os.getpid()}")
        master_socket, addr = to_master_sock.accept()
        print(f"Recived new conn: {master_socket} from {addr}")
        G.master_pool.append(master_socket)
        threading.Thread(target=master_message_handle, daemon=True,args=(master_socket, )).start()




def web_message_handle(web_socket):

    while True:

        print(f"the web message handle pid is {os.getpid()}")
        try:
            data = web_socket.recv(1024).decode()
        except Exception as e:
            print(f"recv from web failed:{e}")
            return
        print(f"[Received from web data]-->>{data}-->> {threading.current_thread().ident}")

        # temp = data.split()
        # msg = temp[-1]
        
        # temp = data.split(TERMINATION_CHAR)
        # print(temp)
        # msg = temp[-2]
        
        G.lock_web_message.acquire()
        G.message_receiced_from_web = True
        G.message_from_web = data
        # if msg == "all on":
        #     G.message_from_web = msg
        #     pass
        # if msg == "all off":
        #     G.message_from_web = "Photoeye:OFF"
        #     pass
        G.lock_web_message.release()

        


def send_to_web(web_socket, message=""):

    message = message + TERMINATION_CHAR
    web_socket.send(message.encode())

def accept_web(to_web_sock: socket.socket):

    while True:
        print(f"the web accept pid is {os.getpid()}")
        web_socket, addr = to_web_sock.accept()
        print(f"Recived new conn: {web_socket} from {addr}")
        G.web_pool.append(web_socket)
        threading.Thread(target=web_message_handle, daemon=True,args=(web_socket, )).start()



def init():

    G.time_alive = time.time()

if __name__ == '__main__':

    init()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localhost = s.getsockname()[0]
    print(f"localhost ip is {localhost}")

    ''' Create sever for master'''
    to_master_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    to_master_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
    to_master_sock.bind((localhost, master_port))

    """ 开启服务 """
    to_master_sock.listen(5)
    print("Waiting for master connection...")

    threading.Thread(target=accept_master, daemon=True,args=(to_master_sock, )).start()

    ''' Create sever for Web'''
    localhost_to_web = socket.gethostname()
    
    to_web_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    to_web_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
    to_web_sock.bind((localhost_to_web, web_port))

    """ 开启服务 """
    to_web_sock.listen(5)
    print("Waiting for web connection...")

    threading.Thread(target=accept_web, daemon=True,args=(to_web_sock, )).start()

    
    G.time_alive  = time.time()
    while True:
        try:
            
            if time.time() - G.time_alive >= 4:
                print(f"the main pid is {os.getpid()}")
                G.time_alive  = time.time()
                if len(G.master_pool):
                    master_socket = G.master_pool[0]
                    try :
                        master_socket.send(ALIVE_FLAG.encode())
                        print("ALIVE EVERY 4 SECOND")
                    except ConnectionResetError as error:
                        print(f"it is disconneted {error}")
            
            if G.message_receiced_from_web == True:
                G.lock_web_message.acquire()            
                G.message_receiced_from_web = False
                G.buff_for_web = G.message_from_web
                print(f"the buff is {G.buff_for_web}")
                G.lock_web_message.release()

                G.buff_for_web = G.buff_for_web + TERMINATION_CHAR
                # G.buff_for_web = G.buff_for_web
                print(f"the buff is {G.buff_for_web}")
                if len(G.master_pool):
                    master_socket = G.master_pool[0]
                    master_socket.send(G.buff_for_web.encode())
                    print(f"sent the{G.buff_for_web} to master")
        except KeyboardInterrupt:
            print("you just pressed control + C, and it exited")
            exit()




   



