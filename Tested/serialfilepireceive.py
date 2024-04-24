#服务器端

from machine import Pin,SPI,UART,I2C,WDT

import struct
import os

def uart_receiver():

    uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1),timeout=1)
    uart.init(bits=8, parity=None, stop=1)
    uart.write(bytes('Bodyguard Pico start...',"utf-8"))
    print("I am here")
    while True:
        if uart.any():
            data2 = uart.read()
            data = data2.decode()
            print(data)
            
            # data2 = uart.read()
            # print(data2)
            # print("I am here 2")
            # # d = data2(struct.calcsize("l"))
            # #print(data2.decode('utf-8'))
            # total_size = struct.unpack("l",data2)
            # print(total_size)
            # print(type(total_size))
            # #uart.write(bytes(total_size,"utf-8"))
            # num  = total_size[0]//1024
            # print(num)
            # #uart.write(bytes(num,"utf-8"))
            # data = b''
            # data2 = b''
            # for i in range(num):
            #     if uart.any():
            #         data2 = uart.read(1024)
            #         uart.write(bytes(data2,"utf-8"))
            #         data += data2
                
            # num = total_size[0]%1024
            # if num > 0:
            #     if uart.any():
            #         data2 = uart.read()
            #         print(data2)
            #         if data2 != None:
            #             data += data2
            # print(data)

            with open("13.py","wb") as f:
                    f.write(data)
            f.close()

if __name__ == "__main__":
     
     uart_receiver()
     print("bye")

    



# while True:
#     print("start.......")
#     uart.read()
#     d = sock.recv(struct.calcsize("l"))
#     total_size = struct.unpack("l",d)
#     num  = total_size[0]//1024
#     data = b''
#     for i in range(num):
#         data += sock.recv(1024)
#     data += sock.recv(total_size[0]%1024)

#     with open("11.py","wb") as f:
#         f.write(data)
#     sock.close()
    

#     if uart.any(): 
#         data2 = uart.read()
#         d = data2(struct.calcsize("l"))
#         total_size = struct.unpack("l",d)

#         num  = total_size[0]//1024
#         data = b''
#         for i in range(num):
#             data2 = uart.read(1024)
#             data += data2
        
#         data += uart.read(total_size[0]%1024)

#         with open("11.py","wb") as f:
#                 f.write(data)


#                 temp1 = command_serial.split(TERMINATION_CHAR)
#                 print(f"command_received {temp1}")
#                 command_serial2 = temp1[-1]

# filepath = "C:/Users/Jasper/pico-master/dhcp.py"
# size =  os.stat(filepath).st_size
# f= struct.pack("l",os.stat(filepath).st_size)
# # client.send(f)
# ser.write(f)
# print(f)
# img = open(filepath,"rb")
# print(img.read())
# ser.write(img.read())
# img.close()