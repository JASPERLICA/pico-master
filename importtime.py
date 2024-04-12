import os
import threading
import network

print(os.__file__)
print(threading.__file__)
print(network.__file__)

#  C:\Users\Jasper\pico-master> python .\importtime.py
# :\Users\Jasper\AppData\Local\Programs\Python\Python311\Lib\os.py
# C:\Users\Jasper\AppData\Local\Programs\Python\Python311\Lib\threading.py
# PS C:\Users\Jasper\pico-master> python .\importtime.py
# Traceback (most recent call last):
#   File "C:\Users\Jasper\pico-master\importtime.py", line 3, in <module>
#     import network
# ModuleNotFoundError: No module named 'network'