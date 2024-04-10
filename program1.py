import os

def main():
    r,w = os.pipe()
    pid=os.fork()
    if pid > 0:
        os.close(r)
        w= os.fdopen(w,"w")
        w.write("hello from program1")
        w.close()
    else:
        os.close(w)
        r = os.fdopen(r)
        print(r.read())
        r.close()
if __name__ == '__main__':
    main()