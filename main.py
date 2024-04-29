#!/opt/bin/lv_micropython
import uos as os
import uerrno as errno
from time import sleep
import machine
iter = os.ilistdir()
#iter = os.listdir()
IS_DIR = 0x4000
IS_REGULAR = 0x8000
index = 0
file_name_list = []
try:
    while True:
        entry = next(iter)
        filename = entry[0]
        if filename == 'version.txt':    
            with open('version.txt',"r+") as f:
                str = f.read()
                if str == "newBodyguardPicoMaster.py":
                    print("new version Bodyguard was found")
                    os.remove("BodyguardPicoMaster.py")
                    print("old version Bodyguard was removed")
                    sleep(0.1)
                    os.rename("newBodyguardPicoMaster.py", "BodyguardPicoMaster.py")
                    print("it has renamed ")
                    f.close()
                    os.remove('version.txt')
                    print("version.txt removed")
                    sleep(0.1)
                    open('version.txt', 'a').close()
                    print("version.txt created")
                    sleep(2)
                    machine.reset()
                else:
                    f.close()
                    break

except StopIteration:
    pass
            
iter_new = os.ilistdir()

try:
    while True:
        entry = next(iter_new)
        filename = entry[0]
        file_type = entry[1]
        print(f"the file {filename} has been found and the type is {file_type}")
        if filename == 'main.py':
            continue
        else:
            if file_type == IS_DIR:
                continue
            else:
                exec(open(filename).read(), globals())
                print(f"the file {filename} has been executed")
        if index == 100:
            break
        index += 1
except StopIteration:
    pass

# type is an integer that specifies the type of the entry, with 0x4000 for directories and 0x8000 for regular files;