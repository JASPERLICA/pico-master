import os


path = os.getcwd()
print(path)
path = os.path.abspath("..")
print(path)
print(type(path))
tt= "python_file_practic.txt"
print(type(tt))
path = os.path.join(path,"python_file_practic.txt")
print(path)
print(os.path.isdir(path))
# if os.path.isdir(path) == True:
if os.path.isfile(path) == True:
    print("it is ture")
    with open(path,"r") as f:
        word = f.read()
        print(word)
        f.close()
    os.remove(path)
    print("removed")
print(path)
newfile = open(path,"w+")
newfile.write("this is my first file 5")
# newfile = open(path,"r+")
# print(newfile.read())
# newfile.flush()
newfile.seek(0)
print(newfile.read())
data = newfile.read()
s=newfile.tell()
print(s,data,len(data)-5)
print("it is rewrite")
newfile.close()

path3 = os.path.join(os.getcwd(), "GeeksForGeeks") 