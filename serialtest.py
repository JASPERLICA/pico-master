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


# 文本格式 (Text Mode)
# 文件以文本格式打开时，默认假设文件内容是可读的文本数据。
# 在文本格式中，读取文件时会将字节数据按照特定的编码方式（如UTF-8）解码成字符串。
# 写入文件时，会将字符串按照特定的编码方式编码为字节数据后存储到文件中。
# 文本格式通常用于处理文本文件，比如常见的文本文档、CSV文件、JSON文件等。

# 二进制格式 (Binary Mode)
# 文件以二进制格式打开时，假设文件内容是字节数据，不关心其内容是否可读。
# 在二进制格式中，读取文件时直接返回字节数据，不进行解码转换。
# 写入文件时，将字节数据直接写入到文件中，不进行编码转换。
# 二进制格式通常用于处理非文本文件，如图像文件、音频文件、视频文件等。
# -----------------------------------
# ©著作权归作者所有：来自51CTO博客作者尼羲的原创作品，请联系作者获取转载授权，否则将追究法律责任
# python文件操作详解
# https://blog.51cto.com/u_11365839/10119761

# 假设有一个图片文件 "image.jpg"，我们分别以文本格式和二进制格式打开该文件，来看看它们的区别。

# with open('image.jpg', 'r') as file:
#     content = file.read()
#     print(content)
# 1.
# 2.
# 3.
# 运行上述代码，会遇到错误，因为我们试图以文本格式打开一个图片文件，而图片文件是二进制数据，不适合以文本格式打开。

# with open('image.jpg', 'rb') as file:
#     content = file.read()
#     print(content)
# 1.
# 2.
# 3.
# 运行上述代码，可以成功以二进制格式读取图片文件，并打印出包含图片字节数据的内容。
# -----------------------------------
# ©著作权归作者所有：来自51CTO博客作者尼羲的原创作品，请联系作者获取转载授权，否则将追究法律责任
# python文件操作详解
# https://blog.51cto.com/u_11365839/10119761


# 读文件 进行读文件操作时，直到读到文档结束符（EOF）才算读取到文件最后，Python会认为字节\x1A(26)转换成的字符为文档结束符（EOF），

#       故使用'r'进行读取二进制文件时，可能会出现文档读取不全的现象。

# 由于文件读写时都有可能产生IOError，一旦出错，后面的f.close()就不会调用。所以，为了保证无论是否出错都能正确地关闭文件，我们可以使用try ... finally来实现：

# try:
#     f = open('/path/to/file', 'r')
#     print(f.read())
# finally:
#     if f:
#         f.close()
# 但是每次都这么写实在太繁琐，所以，Python引入了with语句来自动帮我们调用close()方法：

# with open('/path/to/file', 'r') as f:
#     print(f.read())
# 这和前面的try ... finally是一样的，但是代码更佳简洁，并且不必调用f.close()方法。

# 在计算机内存中，统一使用Unicode编码，当需要保存到硬盘或者需要传输的时候，就转换为UTF-8编码。
# 由于Python的字符串类型是str，在内存中以Unicode表示，一个字符对应若干个字节。
# 如果要在网络上传输，或者保存到磁盘上，就需要把str变为以字节为单位的bytes。
# 可见，1个中文字符经过UTF-8编码后通常会占用3个字节，而1个英文字符只占用1个字节。
# 在操作字符串时，我们经常遇到str和bytes的互相转换。
# 为了避免乱码问题，应当始终坚持使用UTF-8编码对str和bytes进行转换。

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