#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
a='Beautiful, is; better*than\nugly'
# 四个分隔符为：,  ;  *  \n
x= re.split(',|; |\*|\n',a)

print(x)


my_num = 45
print(my_num)
print(f"this 45 is {type(my_num)}")
my_num1 = 45
converted_my_num = str(my_num1)

print(converted_my_num)
print(f"this 45 is {type(converted_my_num)}")

i = 555

print(type(i))

chart = f"data is {i}"

print(chart)
print (type(chart))
chart2= chart.encode()
print(chart2)
print(type(chart2))
chart3 = bytes(chart,'utf-8')
print(chart3)
print(type(chart3))

b = str(i)
print(b)


# >>> 'ABC'.encode('ascii')
# b'ABC'
# >>>'ABC'.encode('utf-8')
# b'ABC'
# >>> '中文'.encode('utf-8')
# b'\xe4\xb8\xad\xe6\x96\x87'
# >>> '中文'.encode('ascii')
# Traceback (most recent call last):
#   File "<input>", line 1, in <module>
# UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)

# 作者：望着星空傻笑
# 链接：https://juejin.cn/post/6844904015935832078
# 来源：稀土掘金
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
# t= i.encode()
# print(t)
# print(type(t))


#串口数值型的数据到uart后要转为ascii编码，避免和字符串混为一摊；
#upperLaserReading = uart1Buffer[1] | (uart1Buffer[2] << 8);
#lowerLaserReading = uart1Buffer[3] | (uart1Buffer[4] << 8);
#sprintf(responseAscii, "%d,%d", lowerLaserReading, upperLaserReading);
#sprintf 把数值变成字符串ASCii
#USART0_write_line(responseAscii)


#  char buffer[50];
#     int a = 10, b = 20, c;
#     c = a + b;
#     sprintf(buffer, "Sum of %d and %d is %d", a, b, c);
 
#     // The string "sum of 10 and 20 is 30" is stored
#     // into buffer instead of printing on stdout
#     printf("%s", buffer);

str = "Line1-abcdef\nLine2-abc\nLine4-abcd\n"
#str -- 分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等。
list1 = str.split('\n')
print(list1)
#['Line1-abcdef', 'Line2-abc', 'Line4-abcd', '']
list1 = str.split()
print(list1)
#['Line1-abcdef', 'Line2-abc', 'Line4-abcd']

str = "Chris_iven+Chris_jack+Chris_lusy"
print (str.split("+"))
print (str.split("_"))


s = '\tale s dd\n'
print(s.strip())

# name=input('please enter your name:').strip()
# if name == 'Jasper':
#     print(name)
# else:
#     print('typo')

# 在计算机内存中（你打开电脑上的一个文件是要从硬盘读取到内存中的），统一使用Unicode编码。
# 在需要保存到硬盘或需要传输时，就转化为UTF-8编码（由上篇文章可知，这样可以节省空间，提高传输速度）。
#             如，在记事本编辑时，从文件读取的UTF-8字符被转化为Unicode字符到内存里，编辑完成，
# 保存时在将内存中的Unicode字符转化为UTF-8保存到文件：
#浏览网页时，服务器会把动态生成的Unicode字符转化为UTF-8字符再传输到浏览器：
# 在python中，字符串是以Unicode编码的，而python的字符串类型是str，
# 内存中以Unicode表示。要在网络上进行传输或保存到磁盘中，就需要将str转化为以字节为单位的bytes。
#b'ABC' 与 'ABC'是不同的，前者是bytes，也叫字节字符串；后者是str，也称为文本字符串。
#前者一个字符占一个字节（中文一个汉字占三个字节），str类型在内存中以Unicode表示，一个字符占若干字节。

# 有时需要用python处理二进制数据，比如存取文件，socket操作时。这时可以用python的struct模块来完成，比如可以用struct处理c语言中的结构体。
#             比如有一个结构体：
#             cpp复制代码struct Header
# {
#     unsigned short id;
#     char[4] tag;
#     unsigned int version;
#     unsigned int count;
# }

#             通过socket.recv接收到了上面的结构体数据，存在字符串s中，bytes格式，现在把它解析出来，可以使用unpack函数：
#             go复制代码import struct
# id, tag, version, count = struct.unpack('!H4s2I', s)

#             !表示网络字节顺序，因为数据是从网络上接收到的，再网络上传送时他是网络字节顺序的。后面的H4s2I表示1个unsigned int，4s表示4字节的字符串，2个unsigned short。
#             同样，也可以使用pack再将本地数据pack成struct格式
#             ss = struct.pack('>I4s2I', id, tag, version, count)
#             pack函数按照指定格式转换成了结构体Header，ss现在是一个字节流，可以通过socket将这个字节流发送出去

# 作者：望着星空傻笑
# 链接：https://juejin.cn/post/6844904015935832078
# 来源：稀土掘金
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

number =0x05
print(bytes([number]))

cmd_hex = [0x01, 0x02, 0x03, 0x04]
cmd_bytes = bytes(cmd_hex) 
print(cmd_bytes)
# print(number.encode('utf-8'))


# bytes 函数返回一个新的 bytes 对象，该对象是一个 0 <= x < 256 区间内的整数不可变序列。它是 bytearray 的不可变版本。

# 语法
# 以下是 bytes 的语法:

# class bytes([source[, encoding[, errors]]])
# 参数
# 如果 source 为整数，则返回一个长度为 source 的初始化数组；
# 如果 source 为字符串，则按照指定的 encoding 将字符串转换为字节序列；
# 如果 source 为可迭代类型，则元素必须为[0 ,255] 中的整数；
# 如果 source 为与 buffer 接口一致的对象，则此对象也可以被用于初始化 bytearray。
# 如果没有输入任何参数，默认就是初始化数组为0个元素。
# 返回值
# 返回一个新的 bytes 对象。

# 实例
# 以下展示了使用 bytes 的实例：

# 实例
# >>>a = bytes([1,2,3,4])
# >>> a
# b'\x01\x02\x03\x04'
# >>> type(a)
# <class 'bytes'>
# >>>
# >>> a = bytes('hello','ascii')
# >>>
# >>> a
# b'hello'
# >>> type(a)
# <class 'bytes'>
# >>>

a1 = "abcd"
a  = list(a1)
print(a)

cmd1 = "START"
serial_cmd = cmd1 + '\r'
encodecmd= serial_cmd.encode()
listcmd =list(cmd1)
print(listcmd)
print(cmd1)
print(serial_cmd)
print(list(serial_cmd))

print(bytes(encodecmd))
print(serial_cmd.encode())
print(bytes(serial_cmd.encode()))
print(bytes(serial_cmd,'utf-8'))


# 文本文件存储的内容是基于字符编码的文件，常见的编码有ASCII、UNICODE等

# Python2.x默认使用ASCII编码
# Python3.x默认使用UTF-8编码

# >>> import sys
# >>> print(sys.getdefaultencoding())
# utf-8

# 万一Python3.x中不能读取文件里面的中文怎么办？

# 解决：编写encoding=”UTF-8”

# 例如：

# file = open("HELLO", encoding="UTF-8")

# print('hello\nrunoob')      # 使用反斜杠(\)+n转义特殊字符
# print(r'hello\nrunoob')     # 在字符串前面添加一个 r，表示原始字符串，不会发生转义
# 这里的 r 指 raw，即 raw string，会自动将反斜杠转义，例如：
# hello
# runoob
# hello\nrunoob
# >>> print('\n')       # 输出空行

# >>> print(r'\n')      # 输出 \n
# \n
# >>>

import sys
print('================Python import mode==========================')
print ('命令行参数为:')
for i in sys.argv:
    print (i)
print ('\n python 路径为',sys.path)

# python列表截取：

# L[-2]：读取列表中倒数第二个元素

# L[-1]：读取列表中倒数第一个元素

# L[1：]：从第二个元素开始截取

# 三、Python列表操作的函数和方法
# 列表操作包含以下函数:
# 1、cmp(list1, list2)：比较两个列表的元素 
# 2、len(list)：列表元素个数 
# 3、max(list)：返回列表元素最大值 
# 4、min(list)：返回列表元素最小值 
# 5、list(seq)：将元组转换为列表 
# 四、列表操作包含以下方法:
# 1、list.append(obj)：在列表末尾添加新的对象
# 2、list.count(obj)：统计某个元素在列表中出现的次数
# 3、list.extend(seq)：在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
# 4、list.index(obj)：从列表中找出某个值第一个匹配项的索引位置
# 5、list.insert(index, obj)：将对象插入列表
# 6、list.pop(obj=list[-1])：移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
# 7、list.remove(obj)：移除列表中某个值的第一个匹配项
# 8、list.reverse()：反向列表中元素
# 9、list.sort([func])：对原列表进行排序

# 	list.remove(obj)
# 移除列表中某个值的第一个匹配项

# 可以使用 del 语句来删除列表的的元素，如下实例：
# 
# 实例(Python 3.0+)
# #!/usr/bin/python3
 
# list = ['Google', 'Runoob', 1997, 2000]
 
# print ("原始列表 : ", list)
# del list[2]
# print ("删除第三个元素 : ", list)

# 此外，也可以使用 bytes() 函数将其他类型的对象转换为 bytes 类型。bytes() 函数的第一个参数是要转换的对象，第二个参数是编码方式，如果省略第二个参数，则默认使用 UTF-8 编码：

# x = bytes("hello", encoding="utf-8")
# 与字符串类型类似，bytes 类型也支持许多操作和方法，如切片、拼接、查找、替换等等。同时，由于 bytes 类型是不可变的，因此在进行修改操作时需要创建一个新的 bytes 对象。例如：

# 实例

# x = b"hello"
# y = x[1:3]  # 切片操作，得到 b"el"
# z = x + b"world"  # 拼接操作，得到 b"helloworld"
# 需要注意的是，bytes 类型中的元素是整数值，因此在进行比较操作时需要使用相应的整数值。例如：

# 实例
# x = b"hello"
# if x[0] == ord("h"):
#     print("The first element is 'h'")
# 其中 ord() 函数用于将字符转换为相应的整数值。


# 问题无外乎就是 python 没有自增运算符，自增操作是如何实现的。

# 回答中有人介绍了关于自增操作，python 不使用 ++ 的哲学逻辑：编译解析上的简洁与语言本身的简洁，就不具体翻译了。

# 后面还有老外回答并附带了一个例子非常的精彩，指出了 python 与 c 语言概念上的一些差异，语言描述的可能未必准确，直接上例子：

# >>> b = 5  
# >>> a = 5  
# >>> id(a)  
# 162334512  
# >>> id(b)  
# 162334512  
# >>> a is b  
# True  
# 可以看出， python 中，变量是以内容为基准而不是像 c 中以变量名为基准，所以只要你的数字内容是5，不管你起什么名字，这个变量的 ID 是相同的，同时也就说明了 python 中一个变量可以以多个名称访问。

# 这样的设计逻辑决定了 python 中数字类型的值是不可变的，因为如果如上例，a 和 b 都是 5，当你改变了 a 时，b 也会跟着变，这当然不是我们希望的。

# 因此，正确的自增操作应该 a = a + 1 或者 a += 1，当此 a 自增后，通过 id() 观察可知，id 值变化了，即 a 已经是新值的名称。

# 纠正一下楼上的一些观点

# 楼上的同学所说的在脚本式编程环境中没有问题。但是在交互式环境中，编译器会有一个小整数池的概念，会把（-5，256）间的数预先创建好，而当a和b超过这个范围的时候，两个变量就会指向不同的对象了，因此地址也会不一样，比如下例：

# >>> a=1000
# >>> b=1000
# >>> id(a);id(b)
# 2236612366224
# 2236617350384


# is 和 ==

# is 判断两个变量是否是引用同一个内存地址。

# == 判断两个变量是否相等。

# 如果不用 a = b 赋值，int 型时，在数值为 -5~256（64位系统）时，两个变量引用的是同一个内存地址，其他的数值就不是同一个内存地址了。

# 也就是，a b 在 -5~256（64位系统）时：

# a = 100
# b = 100
# a is b # 返回 True
# 其他类型如列表、元祖、字典让 a、b 分别赋值一样的时：

# a is b  # 返回False

# >>> a=1222
# >>> b=1222
# >>> a is b
# False
# >>> a == b
# True
# >>>

# >>> a=200
# >>> b=200
# >>> a is b
# True
# >>> a==b
# True
# >>>

# 但是数组则不同，在python之中是没有数组这个数据类型的。它是由python内的第三方库科学计算库numpy中的函数所生成的，示例如下：

# import numpy as np
# arr = np.array([1,2])    # arr就是一个数组
# 数组运算
# a = np.array([1,2])
# b = a + a
# [2 4]
# # 列表拼接
# x = [1,2,'a']
# y = x + x
# [1, 2, 1, 2]

# 数字与字符，列表之间的转换

# 1、字符转为数字

# var='1234'
# num=int(var) # 如果是小数可用 float
# 2、字符转为列表

# num_list=list(var)
# 3、列表转为数组

# 可以用 numpy 模块：

# import numpy as np

# num_array=np.array(num_list)
# 也可以是 num_array=[int(i) for i in num_list]。

# \(在行尾时)	续行符

# print("\a") \a	响铃

# \r	回车，将 \r 后面的内容移到字符串开头，并逐一替换开头部分的字符，直至将 \r 后面的内容完全替换完成。

# import time

# for i in range(101):
#     print("\r{:3}%".format(i),end=' ')
#     time.sleep(0.05)


str1 = "adfadsf"
for each in str1:
    print(each)

for each in str1:
    print(each,end = "")

    Python 3.x
# 在 Python 3.x 中，我们可以在 print() 函数中添加 end="" 参数，这样就可以实现不换行效果。

# 在 Python3 中， print 函数的参数 end 默认值为 "\n"，即end="\n"，表示换行，给 end 赋值为空, 即end=""，就不会换行了，例如：

# Python3.x 实例
# print('这是字符串，', end="")
# print('这里的字符串不会另起一行')

# Unicode 字符串
# 在Python2中，普通字符串是以8位ASCII码进行存储的，而Unicode字符串则存储为16位unicode字符串，这样能够表示更多的字符集。使用的语法是在字符串前面加上前缀 u。

# 在Python3中，所有的字符串都是Unicode字符串。

# Python 的字符串内建函数 https://www.runoob.com/python3/python3-string.html

# 如果是I/O 密集型，且I/O 请求比较耗时的话，使用协程。 
# 如果是I/O 密集型，且I/O 请求比较快的话，使用多线程。 
# 如果是计算密集型，考虑可以使用多核CPU，使用多进程

# aList = [123, 'xyz', 'runoob', 'abc']

# print "xyz 索引位置: ", aList.index( 'xyz' )
# print "runoob 索引位置 : ", aList.index( 'runoob', 1, 3 )
# 以上实例输出结果如下：

# xyz 索引位置:  1
# runoob 索引位置 :  2

# 通过 values 取到 key 的方法：

# >>> dic={"a":1,"b":2,"c":3}
# >>> list(dic.keys())[list(dic.values()).index(1)]
# 'a'

# 如果 if 语句中的条件过长，可以用接续符 \ 来换行。

# 例如：

# if 2>1 and 3>2 and 4>3 and \
#     5>4 and 6>5 and 7>6 and \
#     8>7:
#     print("OK")
# 注意: \ 后的一行要缩进没有要求，可无序缩进，但我们保持代码的可读性一般设置同样的缩进格式。

# 上一篇总结os模块，该模块与 sys 模块从名称上看着好像有点类似，实际上关系不大，
# os 模块主要负责与操作系统进行交互，而这个两个模块常常搭配起来使用， 能实现许多需求。
# sys 模块主要负责与 Python 解释器进行交互，提供了一系列用于控制 Python 运行环境的函数和变量。
# 本文为常用的sys模块用法总结
# 1、sys.argv: 实现从程序外部向程序传递参数。

# 2、sys.exit([arg]): 程序中间的退出，arg=0为正常退出。

# 3、sys.getdefaultencoding(): 获取系统当前编码，一般默认为ascii。

# 4、sys.setdefaultencoding(): 设置系统默认编码，执行dir（sys）时不会看到这个方法，在解释器中执行不通过，可以先执行reload(sys)，在执行 setdefaultencoding('utf8')，此时将系统默认编码设置为utf8。（见设置系统默认编码 ）

# 5、sys.getfilesystemencoding(): 获取文件系统使用编码方式，Windows下返回'mbcs'，mac下返回'utf-8'.

# 6、sys.path: 获取指定模块搜索路径的字符串集合，可以将写好的模块放在得到的某个路径下，就可以在程序中import时正确找到。

# 7、sys.platform: 获取当前系统平台。

# 8、sys.modules：是一个全局字典，该字典是python启动后就加载在内存中。每当程序员导入新的模块，sys.modules将自动记录该模块。当第二次再导入该模块时，python会直接到字典中查找，从而加快了程序运行的速度。它拥有字典所拥有的一切方法。

# 9、sys.stdin,sys.stdout,sys.stderr: stdin , stdout , 以及stderr 变量包含与标准I/O 流对应的流对象. 如果需要更好地控制输出,而print 不能满足你的要求, 它们就是你所需要的. 你也可以替换它们, 这时候你就可以重定向输出和输入到其它设备( device ), 或者以非标准的方式处理它们


# 里面有个 sys.path属性。他是一个list.默然情况下python导入文件或者模块的话，他会先在sys.path里找模块的路径。如果没有的话，

# 程序就会报错。

# 所以我们一般自己写程序的话。最好把自己的模块路径给加到当前模块扫描的路径里,eg: sys.path.append('你的模块的名称'),这样程序就不会

# 因为找不到模块而报错。。

# 当你导入一个模块，Python 解析器对模块位置的搜索顺序是

# 当前目录
# 如果在当前目录没有找到，Python 则搜索在 shell 变量 PYTHONPATH 下的每个目录
# 如果都找不到，Python会查看默认路径。UNIX下，默认路径一般为/usr/local/lib/python/
# 模块搜索路径存储在 system 模块的 sys.path 变量中。变量里包含当前目录，PYTHONPATH和由安装过程决定的默认目录。

# 'C:\\Users\\Jasper\\AppData\\Local\\Programs\\Python\\Python311\\Lib
# C:\Users\Jasper\AppData\Local\Programs\Python\Python311\
# 当导入模块时系统会自动按顺序从这些路径搜索一遍看看是否存在，如果用户想导入自己的写的模块也可以操作的。
# 可以发现这个是一个列表，所以支持列表操作，如果想导入当前目录下的模块，可以使用列表增加元素的操作

# sys.path.append('path')
# path是你要导入的路径
# 例如我导入/Documents/practice

# In [8]: sys.path.append('/Documents/practice')
 
# In [9]: sys.path
# Out[9]: 
# ['',
#  '/usr/bin',
#  '/usr/local/lib/python3.5/dist-packages/pygame-1.9.4.dev0-py3.5-linux-x86_64.egg',
#  '/usr/lib/python35.zip',
#  '/usr/lib/python3.5',
#  '/usr/lib/python3.5/plat-x86_64-linux-gnu',
#  '/usr/lib/python3.5/lib-dynload',
#  '/home/am/.local/lib/python3.5/site-packages',
#  '/usr/local/lib/python3.5/dist-packages',
#  '/usr/lib/python3/dist-packages',
#  '/usr/lib/python3/dist-packages/IPython/extensions',
#  '/home/am/.ipython',
#  '/Documents/practice']

# 3、环境变量的作用
# 刚才说过，1、随着电脑安装的软件越来越多，我们记不住所有软件的安装路径，想运行某一软件就很麻烦
# 。2、如果想在某一路径下直接运行某款软件，我们无能为力。

# 通过在环境变量里面加入所有软件的安装路径，当我们想运行某一软件时双击其快捷方式或者在DOS界面输入软件名称，
# 此时，计算机除了在其当前目录下寻找该软件的.exe文件外，还在环境变量中搜索软件的路径，找到，运行。

# 综上，Windows和DOS操作系统中的path环境变量，当要求系统运行一个程序而没有告诉它程序所在的完整路径时，
# 系统除了在当前目录下面寻找此程序外，还应到path中指定的路径去找。用户通过设置环境变量，来更好的运行进程。

# 1. 获取命令行参数
# sys.argv 是一个包含命令行参数的列表，其中第一个元素是脚本的名称。

# import sys

# # 示例脚本名为 example.py
# print("Script Name:", sys.argv[0])

# # 打印所有命令行参数
# print("Command Line Arguments:", sys.argv[1:])
# 2. 修改默认编码
# sys 模块允许修改默认的字符串编码，这对于处理不同编码的数据非常有用。

# import sys

# # 查看默认编码
# print("Default Encoding:", sys.getdefaultencoding())

# # 修改默认编码为UTF-8
# sys.setdefaultencoding("utf-8")

# 再次查看默认编码
# print("Updated Encoding:", sys.getdefaultencoding())
# 3. 强制退出程序
# 通过 sys.exit() 可以在程序中任意位置强制退出，可传入整数参数作为退出状态码。

# import sys

# def example_function():
#     print("Function is running.")
#     sys.exit(1)

# example_function()
# print("This line will not be executed.")
# 4. 获取Python解释器版本信息
# sys.version 提供了当前 Python 解释器的版本信息。

# import sys

# print("Python Version:", sys.version)
# 5. 改变模块搜索路径
# sys.path 包含了一个列表，其中存储了 Python 解释器用来查找模块的路径。

# import sys

# # 打印当前模块搜索路径
# print("Current Path:", sys.path)

# # 添加新的路径
# sys.path.append("/path/to/new/module")
# print("Updated Path:", sys.path)
# 6. 重定向标准输入输出流
# 通过 sys.stdin、sys.stdout 和 sys.stderr 可以重定向标准输入、标准输出和标准错误流。

# import sys

# # 保存原始的标准输出流
# original_stdout = sys.stdout

# # 重定向标准输出到文件
# with open("output.txt", "w") as f:
#     sys.stdout = f
#     print("This will be written to output.txt")

# # 恢复原始的标准输出流
# sys.stdout = original_stdout
# print("This will be printed to the console.")
# 7. 获取系统相关信息
# sys 模块提供了一些关于系统的基本信息，如平台、版本等。

# import sys

# print("Platform:", sys.platform)
# print("Version:", sys.version_info)
# 8. 获取当前模块
# sys.modules 是一个字典，包含了当前载入的所有模块。

# import sys

# # 获取当前模块的信息
# current_module = sys.modules[__name__]
# print("Current Module:", current_module)
# 9. 自定义异常处理
# 通过 sys.exc_info() 可以获取当前异常信息，用于自定义异常处理。

# import sys

# try:
#     x = 1 / 0
# except ZeroDivisionError:
#     exc_type, exc_value, exc_traceback = sys.exc_info()
#     print(f"Exception Type: {exc_type}")
#     print(f"Exception Value: {exc_value}")
#     print(f"Exception Traceback: {exc_traceback}")
# 10. 清理资源
# sys 模块中的 sys.exitfunc 是一个函数列表，用于在解释器退出之前执行清理操作。

# import sys

# def cleanup_function():
#     print("Cleaning up resources.")

# # 将清理函数添加到 exitfunc 列表
# sys.exitfunc = cleanup_function

# # 退出程序时会调用清理函数
# sys.exit(0)


0、__init__.py
# 在Python工程里，当python检测到一个目录下存在__init__.py文件时，python就会把它当成一个模块(module)。
# Module跟C＋＋的命名空间和Java的Package的概念很像，都是为了科学地组织化工程，管理命名空间
#
# @file __init__.py
#

# import arithmetic.add
# import arithmetic.sub
# import arithmetic.mul
# import arithmetic.dev

# add = arithmetic.add.add
# sub = arithmetic.sub.sub
# mul = arithmetic.mul.mul
# dev = arithmetic.dev.dev
# 在__init__.py中， 我们import了arithmetic下的所有子模块，
# 并在__init__.py中给各个子模块的核心功能取了新的名字，作为arithmetic模块的变量。
# 所以我们在main.py中import了arithmetic模块之后，就可以直接进行使用了。
# 如果你使用from arithmetic import * 语句，那么我们就可以使用add、sub、mul、dev，连a4都省了

# Python两种输出值的方式: 表达式语句和 print() 函数。

# 第三种方式是使用文件对象的 write() 方法，标准输出文件可以用 sys.stdout 引用。


# 语法错误
# 这个例子中，函数 print() 被检查到有错误，是它前面缺少了一个冒号 : 。

# 语法分析器指出了出错的一行，并且在最先找到的错误的位置标记了一个小小的箭头。
# 异常
# 即便 Python 程序的语法是正确的，在运行它的时候，也有可能发生错误。运行期检测到的错误被称为异常。

# 大多数的异常都不会被程序处理，都以错误信息的形式展现在这里:


类的方法与普通的函数只有一个特别的区别——它们必须有一个额外的第一个参数名称, 按照惯例它的名称是 self。

class Test:
    def prt(self):
        print(self)
        print(self.__class__)
 
t = Test()
t.prt()
以上实例执行结果为：

<__main__.Test instance at 0x100771878>
__main__.Test
从执行结果可以很明显的看出，self 代表的是类的实例，代表当前对象的地址，而 self.class 则指向类。

# self 不是 python 关键字，我们把他换成 runoob 也是可以正常执行的:

# class Test:
#     def prt(runoob):
#         print(runoob)
#         print(runoob.__class__)
 
# t = Test()
# t.prt()
# 以上实例执行结果为：

# <__main__.Test instance at 0x100771878>
# __main__.Test

# 在 Python中，self 是一个惯用的名称，用于表示类的实例（对象）自身。它是一个指向实例的引用，使得类的方法能够访问和操作实例的属性。

# 当你定义一个类，并在类中定义方法时，第一个参数通常被命名为 self，尽管你可以使用其他名称，但强烈建议使用 self，以保持代码的一致性和可读性。

# 实例

#!/usr/bin/python3
 
#类定义
# class people:
#     #定义基本属性
#     name = ''
#     age = 0
#     #定义私有属性,私有属性在类外部无法直接进行访问
#     __weight = 0
#     #定义构造方法
#     def __init__(self,n,a,w):
#         self.name = n
#         self.age = a
#         self.__weight = w
#     def speak(self):
#         print("%s 说: 我 %d 岁。" %(self.name,self.age))
 
# # 实例化类
# p = people('runoob',10,30)
# p.speak()

最新的 Python3.7 中(2018.07.13)，对类的构造函数进行了精简。

# 3.7 版本：

# from dataclasses import dataclass
# @dataclass
# class A:
#   x:int
#   y:int
#   def add(self):
#     return self.x + self.y
# 相当于以前的：

# class A:
#   def __init__(self,x,y):
#     self.x = x
#     self.y = y
#   def add(self):
#     return self.x + self.y


# Python3 标准库概览
# Python 标准库非常庞大，所提供的组件涉及范围十分广泛，使用标准库我们可以让您轻松地完成各种任务。

# 以下是一些 Python3 标准库中的模块：

# os 模块：os 模块提供了许多与操作系统交互的函数，例如创建、移动和删除文件和目录，以及访问环境变量等。

# sys 模块：sys 模块提供了与 Python 解释器和系统相关的功能，例如解释器的版本和路径，以及与 stdin、stdout 和 stderr 相关的信息。

# time 模块：time 模块提供了处理时间的函数，例如获取当前时间、格式化日期和时间、计时等。

# datetime 模块：datetime 模块提供了更高级的日期和时间处理函数，例如处理时区、计算时间差、计算日期差等。

# random 模块：random 模块提供了生成随机数的函数，例如生成随机整数、浮点数、序列等。

# math 模块：math 模块提供了数学函数，例如三角函数、对数函数、指数函数、常数等。

# re 模块：re 模块提供了正则表达式处理函数，可以用于文本搜索、替换、分割等。

# json 模块：json 模块提供了 JSON 编码和解码函数，可以将 Python 对象转换为 JSON 格式，并从 JSON 格式中解析出 Python 对象。

# urllib 模块：urllib 模块提供了访问网页和处理 URL 的功能，包括下载文件、发送 POST 请求、处理 cookies 等。

# import os

# # 获取当前工作目录
# current_dir = os.getcwd()
# print("当前工作目录:", current_dir)

# # 列出目录下的文件
# files = os.listdir(current_dir)
# print("目录下的文件:", files)

# 所有的数据类型，值，变量，函数，类，实例等等一切可操作的基本单元在 Python 都使用对象（Object）表示。每个对象有三个基本属性：ID，类型和值，也即有一块内存中存储了一个对象，这块内存中一定存有这三个属性。

# a = 1
# print(id(a), type(a), a)
# print(id(int), type(int), int)
# print(id(type), type(type), type)

# >>>
# 1384836208 <class 'int'> 1
# 1837755504 <class 'int'> 1
# 1837581680 <class 'type'> <class 'int'>
# 1837610960 <class 'type'> <class 'type'>


# def test_args(*args, **kwargs):
#     print(args)
#     print(kwargs)

# test_args(1, 2, {"key0": "val0"}, name="name", age=18)

# >>>
# (1, 2, {'key0': 'val0'})
# {'name': 'name', 'age': 18}


#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import os, sys

# # 列出目录
# print "目录为: %s"%os.listdir(os.getcwd())

# # 重命名
# os.rename("test","test2")

# print "重命名成功。"

# # 列出重命名后的目录
# print "目录为: %s" %os.listdir(os.getcwd())

# 目录为:
# [  'a1.txt','resume.doc','a3.py','test' ]
# 重命名成功。
# [  'a1.txt','resume.doc','a3.py','test2' ]

# PICO 库文件 阅读
# http://www.86x.org/en/latet/library/index.html#

# array – 数值数据数组
# binascii – 二进制/ASCII 转换
# builtins – 内置函数和异常
# cmath – 复数的数学函数
# collections – 集合和容器类型
# errno – 系统错误代码
# gc – 控制垃圾收集器
# hashlib – 散列算法
# heapq – 堆队列算法
# io – 输入/输出流
# json – JSON 编码和解码
# math – 数学函数
# os – 基本的“操作系统”服务
# re – 简单的正则表达式
# select – 等待一组流上的事件
# socket – 插座模块
# ssl – SSL/TLS 模块
# struct – 打包和解包原始数据类型
# sys – 系统特定功能
# time – 时间相关功能
# uasyncio — 异步 I/O 调度器
# zlib – zlib 解压
# _thread – 多线程支持

# MicroPython 特定的库
# 以下库中提供了特定于 MicroPython 实现的功能。

# bluetooth — 低级蓝牙
# btree – 简单的 BTree 数据库
# cryptolib – 密码密码
# framebuf —帧缓冲区操作
# machine — 与硬件相关的功能
# micropython – 访问和控制 MicroPython 内部结构
# neopixel — WS2812 / NeoPixel LED 的控制
# network — 网络配置
# uctypes – 以结构化的方式访问二进制数据