import serial
from xmodem import XMODEM
import os
 
def Send_File(filepath, port='COM8', baudrate=115200):
    bn = os.path.basename(filepath)
    filesize = os.stat(filepath).st_size
    strSendFileCMD = "AFF_" + str(filesize) + "_" + bn + "\n"
    # 打开串口
    ser = serial.Serial(port, baudrate)
     
    # 定义YMODEM发送函数
    def send_ymodem(filename):
        def getc(size, timeout=1):
            return ser.read(size)
        def putc(data, timeout=1):
            return ser.write(data)
        modem = XMODEM(getc, putc)
        with open(filename, "rb") as f:
            status = modem.send(f)
        return status
     
    # 发送指令
    ser.write(strSendFileCMD.encode())
    # 发送文件
    status = send_ymodem(filepath)
    if status:
        print(f"文件发送成功：{filepath}")
    else:
        print(f"文件发送失败：{filepath}")
    # 关闭串口
    ser.close()
 
 
def Recv_File(port='COM2', baudrate=115200):
    # 打开串口
    ser = serial.Serial(port, baudrate)
     
    # 定义YMODEM接收函数
    def recv_ymodem(filename):
        def getc(size, timeout=1):
            return ser.read(size) or None
        def putc(data, timeout=1):
            return ser.write(data)
        modem = XMODEM(getc, putc)
        with open(filename, "wb") as f:
            status = modem.recv(f)
        return status
     
    # 循环监听指令
    while True:
        # 接收指令
        print("等待接收指令")
        strCMD = ser.read_until().strip().decode()
        print(strCMD)
        cmdlist = strCMD.split("_")
        cmd = cmdlist[0]
        filesize = cmdlist[1]
        filename = cmdlist[2]
        if cmd == "AFF":
            # 收到指令后开始接收文件
            print("开始接收文件")
            # 接收文件并保存
            status = recv_ymodem(filename)
            if status:
                print(f"文件接收成功：{filename}")
            else:
                print(f"文件接收失败：{filename}")
            # 继续监听指令
            continue
        # 其他指令
        print(f"收到指令：{cmd}")
    # 关闭串口
    ser.close()
 
if __name__=="__main__":
    Send_File("D:/users.7z") #发送文件
    #Recv_File() #接收文件