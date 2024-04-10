import os

def main():
    r,w = os.pipe()
    pid=os.fork()
    if pid > 0:
        os.close(w)
        r = os.fdopen(r)
        print(r.read())
        r.close()
       
    else:
        os.close(r)
        
        w= os.fdopen(w,"w")
        w.write("hello from program2")
        w.close()
if __name__ == '__main__':
    main()