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