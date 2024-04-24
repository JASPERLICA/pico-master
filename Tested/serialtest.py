import serial
import serial.tools.list_ports
import struct
import os,time

NAME_OF_USB = "CH340"

# 获取所有串口设备实例。
# 如果没找到串口设备，则输出：“无串口设备。”
# 如果找到串口设备，则依次输出每个设备对应的串口号和描述信息。
ports_list = list(serial.tools.list_ports.comports())
if len(ports_list) <= 0:
    print("无串口设备。")
else:
    print("可用的串口设备如下：")
    for comport in ports_list:
        print(list(comport)[0], "--->>",list(comport)[1])
        if NAME_OF_USB in list(comport)[1]:
            number_of_port = list(comport)[0]
            print (f"the number_of_port is {number_of_port}")

    
# 方式1：调用函数接口打开串口时传入配置参数

ser = serial.Serial(number_of_port, 115200)    # 打开COM17，将波特率配置为115200，其余参数使用默认值
if ser.isOpen():                        # 判断串口是否成功打开
    print("打开串口成功。")
    print(ser.name)    # 输出串口号
else:
    print("打开串口失败。")

filepath = "C:/Users/Jasper/pico-master/BodyguardPicoMasterNew.py"
with open(filepath, 'rb') as file:
    content = file.read()  # 读取文件内容
    print(content)
    print(type(content))
    ser.write(content)
    # ser.write(bytes(content,"utf-8"))
ser.close()

# # 打开 COM17，将波特率配置为115200，数据位为7，停止位为2，无校验位，读超时时间为0.5秒。
# ser = serial.Serial(port="COM17",
#                     baudrate=115200,
#                     bytesize=serial.SEVENBITS,
#                     parity=serial.PARITY_NONE,
#                     stopbits=serial.STOPBITS_TWO,
#                     timeout=0.5) 
 

# ser = serial.Serial("COM17", 115200)    # 打开 COM17，将波特率配置为115200，其余参数使用默认值
# if ser.isOpen():                        # 判断串口是否成功打开
#     print("打开串口成功。")
# else:
#     print("打开串口失败。")
 
# ser.close()
# if ser.isOpen():                        # 判断串口是否关闭
#     print("串口未关闭。")
# else:
#     print("串口已关闭。")



# size =  os.stat(filepath).st_size
# f= struct.pack("l",os.stat(filepath).st_size)
# # client.send(f)
# ser.write(f)
# print(f)








# img = open(filepath,"rb")






# print(img.read())
# time.sleep(1)
# ser.write(img.read())
# img.close()
    # client.close()

 




# # 串口发送 ABCDEFG，并输出发送的字节数。
# write_len = ser.write("ABCDEFG".encode('utf-8'))
# print("串口发出{}个字节。".format(write_len))
# print(f"send out the words as:{write_len}")
 




 
# # 打开 COM17，将波特率配置为115200, 读超时时间为1秒
# ser = serial.Serial(port="COM17", baudrate=115200, timeout=1)
 
# # 读取串口输入信息并输出。
# while True:
#     com_input = ser.read(10)
#     if com_input:   # 如果读取结果非空，则输出
#         print(com_input)
 
# ser.close()