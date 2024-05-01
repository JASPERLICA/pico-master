# import time
# from threading import Thread
 
 
# class AddTask(Thread):
 
#     def __init__(self):
#         super().__init__()
#         self.sum_num = 0
#         self._button = True
 
#     def run(self):
#         print('Begin to add ...')
#         while self._button:
#             print('Sleep start...')
#             time.sleep(10)
#             print('Sleep end...')
#             self.sum_num += 10
#         print(f"Finish add, sum:{self.sum_num}...")
 
#     def stop(self):
#         print('Stop task...')
#         self._button = False
 
 
# def do_main_task():
#     print('Do main task...')
#     time.sleep(15)
#     print('Finish main task...')
#     return True
 
 
# if __name__ == '__main__':
#     add_task = AddTask()
#     add_task.start()
#     main_task_end = do_main_task()
#     if main_task_end:
#         add_task.stop()
#         time.sleep(1)
#         print(f"sum: {add_task.sum_num}")


import time
from datetime import datetime
from threading import Thread
from threading import Event
 
 
class AddTask(Thread):
 
    def __init__(self):
        super().__init__()
        self.sum_num = 0
        self.event = Event()
        self.time_process = datetime.now().time()
 
    def run(self):
        print('Begin to add ...')
        while not self.event.is_set():
        # while True:
            print(f'Sleep start...{datetime.now().time()}')
            self.event.wait(5) 
            # time.sleep(5)
            print(f'Sleep end...{datetime.now().time()}')
            self.sum_num += 5
        print(f"Finish add, at the time {datetime.now().time()} sum:{self.sum_num}...")
 
    def stop(self):
        print(f'Stop task...{datetime.now().time()}')
        self.event.set()
 
 
def do_main_task():
    print(f'Do main task...{datetime.now().time()}')
    time.sleep(7)
    print(f'Finish main task...{datetime.now().time()}')
    return True
 
 
if __name__ == '__main__':
    time_begin = datetime.now().time()
    print(time_begin)
    add_task = AddTask()
    # add_task.setDaemon(True)
    add_task.start()
    main_task_end = do_main_task()
    try:
        if main_task_end:
            add_task.stop()
            time.sleep(1)
            print(f"sum: {add_task.sum_num} at {datetime.now().time()}")
    except KeyboardInterrupt:
        exit(1)
