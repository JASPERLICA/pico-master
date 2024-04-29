import os
# import sys
# sys.path.append("..")
# from Pico_over_air import ota

# firmware_url = "https://raw.githubusercontent.com/JASPERLICA/pico_ota/main/"

# ota_updater = ota.OTAUpdater(firmware_url, "main.py","version.json")

path = os.path.abspath("file_test.py")
print(path)
path2 = os.getcwd()
print(path2)
#找到所有的文件
for file in os.listdir(os.getcwd()):
    if file.endswith(".txt"):
        print(file)
    
    if file.startswith("file"):
        print(file)

print("new motheds .................")

#找到所有的文件连通路径
for file in os.listdir(os.getcwd()):
    path_temp = os.path.join(os.getcwd(),file)
    if(path_temp[path_temp.rfind(".")+1:] == "txt"):
        print(path_temp)

def number_play(number):
    print(number)
    if number == 1:
        return
    else:
        number_play(number-1)

number_play(16)