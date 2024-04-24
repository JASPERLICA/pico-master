#服务器端
import socket
import struct
try:
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("127.0.0.1",3008))
    server.listen(3)
    while True:
        print("start.......")
        sock,adddr = server.accept()
        d = sock.recv(struct.calcsize("l"))
        print(d)
        total_size = struct.unpack("l",d)
        print(total_size)
        num  = total_size[0]//1024
        print(num)
        data = b''
        for i in range(num):
            data += sock.recv(1024)
        data += sock.recv(total_size[0]%1024)

        with open("12.py","wb") as f:
            f.write(data)
        sock.close()
except KeyboardInterrupt:
    print("ctrl +C was pressed")

    sock.close()