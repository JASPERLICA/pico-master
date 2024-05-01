Python 程序积累

No 1
list(range(1, 11))
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#####################################
>>> L = []
>>> for x in range(1, 11):
...   L.append(x * x)
...
>>> L
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

No 2 列表生成式
[x * x for x in range(1, 11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
No 3
import os # 导入os模块，模块的概念后面讲到
>>> [d for d in os.listdir('.')] # os.listdir可以列出文件和目录
No 4
d = {'x': 'A', 'y': 'B', 'z': 'C' }
>>> for k, v in d.items():
No 5
L = ['Hello', 'World', 'IBM', 'Apple']
>>> [s.lower() for s in L]
['hello', 'world', 'ibm', 'apple']
No 6
>>> x = 'abc'
>>> y = 123
>>> isinstance(x, str)
True
>>> isinstance(y, str)
False
