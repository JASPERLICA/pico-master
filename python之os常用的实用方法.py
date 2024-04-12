python之os常用的实用方法
运维朱工
运维朱工
9 人赞同了该文章
os模块在自动化很有用，可以完成很多鼠标做的事，比如爬到的数据自动新建文件打包等。

正式开始介绍：(ps:用之前要导入。)

1，得到当前的工作目录的路径。 os.getcwd( )

>>> import os
>>> os.getcwd()
'C:\\Program Files\\Python36-32'  #我目前的工作路径
2，由上可以得到当前工作路径的文件列表。 os.listdir(os.getcwd())

>>> os.listdir(os.getcwd())
['.check.txt', 'DLLs', 'Doc', 'include', 'Lib', 'libs', 'LICENSE.txt', 'NEWS.txt', 'python.exe', 'python3.dll', 'python36.dll', 'pythonw.exe', 'Scripts', 'selenium', 'tcl', 'Tools', 'vcruntime140.dll']
3，删除文件。 os.remove()

#os.remove(文件名)  #要是文件不在当前目录，就是使用绝对路径了。
try:
    os.remove("C:\\Users\\Administrator\\Desktop\\123.txt")
    print("OK")  #注意了，路径一定要用引号啊，不然就是语法错误了。如果本来没有文件或者路径错了，会报错找不到。  
except Exception as e:
    print(e)
#执行结果。
OK
>>>
 #又执行了一遍，因为刚才的文件已经删了，所以报错，找不到文件。
[WinError 2] 系统找不到指定的文件。: 'C:\\Users\\Administrator\\Desktop\\123.txt'
>>> 
4，获得绝对路径。 os.path.abspath(文件名)

>>> os.path.abspath("test1")
'C:\\Users\\Administrator\\Desktop\\test1'
5，运行shell命令。 os.system()

>>> os.system("cmd")  #直接运行dos系统
6，要是忘了使用的系统是用那种路径分割符，可以用这个查下。 os.sep

>>> os.sep
'\\'     #用的是双反斜杠，其实是用“\”转义的
7，将一个路径的目录名和文件名分开。 os.path.split()

>>> os.path.split("C:\\Users\\Administrator\\Desktop\\test1.py")
('C:\\Users\\Administrator\\Desktop', 'test1.py')  #提取文件
8，将一个文件名与扩展名分开。 os.path.splitext()

>>> os.path.splitext("test1.py")
('test1', '.py')
9，创建文件。 os.mkdir()

>>> os.mkdir("test")    #在当前工作路径创建了一个test文件夹
如果想在指定路径创建呢，只需要把路径地址填在文件夹前面即可，也是在双引号内。

import os
try:
    name = "python3"
    dir_ = os.mkdir("C:\\Users\\Administrator\\Desktop\\%s"%name)#在桌面建了一个python3的文件夹
except Exception as e:
    print(e)
10，如果想批量一个嵌套的文件，即在一个新建的文件里面，在建文件夹。 os.makedirs()

import os
try:
    name = "python3"
    count = 1
    for i in range(3):
        os.makedirs("%s/first%d"%(name,count))#这里面可以直接写文件名，之所以没有写\
是因为后期也很少会写，因为是批量行为，所以不能写死了。直接调用，自动生成文件名。
        count += 1
except Exception as e:
    print(e)

11，既然创建了，就是为了读取文件。要想读取文件夹下的所有文件，就用到这个了。

import os
try:
    path = "D:/360Downloads/leaningpython/Day10/python3/first1"#文件夹地址
    files = os.listdir(path)  #可以获取文件夹里的所有文件名
    for i in files:
        print(i)   #提示下面读取的是哪个文件
        if not os.path.isdir(i):   #判读文件不是文件夹，如果不是，就读取。
            f = open(path + "/" + i ,"r")   #开始打开文件
            for line in f:  
                print(line.strip())  #打印出来，strip去除空格和换行符
except Exception as e:
    print(e)

13，既然可以打印出来就可以写入另一个文件。相当于把几个文件夹的内容整合。

import os
try:
    path = "D:/360Downloads/leaningpython/Day10/python3/first1"
    files = os.listdir(path)  #找出该目录下的所有文件
    for i in files:
        if not os.path.isdir(i):  #找出不是文件夹的文件
            f = open(path + "/" + i ,"r")  #对文件进行读取
            file3 = open(path + "/第三个文件.txt", "a")  #用追加方式创建新文件并写入
            file3.write("\n"+i +"\n")    #提示当前写入的内容来自哪个文件，并且起到末尾换行的作用，\
不然第二个文件内容写入会在末尾追加.层次混乱
            for line in f:
                file3.write(line)
            file3.close()   #一定要关闭文件
    with open(path + "/第三个文件.txt", "r") as file4:
        print(file4.read().strip())    #可读可不读，这里是为了验证新文件内容是否正确
except Exception as e:
    print(e)