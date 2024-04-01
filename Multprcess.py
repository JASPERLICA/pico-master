#https://realpython.com/python-gil/
from multiprocessing import Pool
import time

COUNT = 50000000
def countdown(n):
    while n>0:
        n -= 1

if __name__ == '__main__':
    pool = Pool(processes=2)
    start = time.time()
    r1 = pool.apply_async(countdown, [COUNT//2])
    r2 = pool.apply_async(countdown, [COUNT//2])
    pool.close()
    pool.join()
    end = time.time()
    print('Time taken in seconds -', end - start)

# PS C:\Users\Jasper\pico-master> python .\multi_threaded.py
# Time taken in seconds - 5.886393785476685
# PS C:\Users\Jasper\pico-master> python .\single_threaded.py
# Time taken in seconds - 5.762033462524414
# PS C:\Users\Jasper\pico-master> python .\Multprcess.py    
# Time taken in seconds - 4.5704872608184814
# PS C:\Users\Jasper\pico-master> 