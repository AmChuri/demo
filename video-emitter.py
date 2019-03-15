import socket  # Import socket module
import os







port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
# s = socket.socket()  # Create a socket object
host = '192.168.122.30'  # Get local machine name
# s.bind((host, port))  # Bind to the port

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
count = 1;
filecount = 1
videoNum = 1000
byteRead = 3072 #total number of bytes read/send per transfer

while True:

    # s.listen(5)  # Now wait for client connection.
    # print('Server listening....')
    # conn, addr = s.accept()  # Establish connection with client.
    # print('Got connection from', addr)


    filename = 'data/f'+str(filecount)+'.mp4'  # In the same folder or path is this file running must the file you want to tranfser to be
    print('filename ',filename)
    filename = 'data/a.mp4'
    f = open(filename, 'rb')
    l = f.read(byteRead)
    while (l):
        count += 1
        # conn.send(l)
        s.sendto(l, (host, port))
        l = f.read(byteRead)
    f.close()

    print("End ",count)
    # s.sendto(b'END', (host, port))  # send empty byte to inform about closing file
    filecount +=1
    print('Done sending')
    # conn.close()
    if filecount == videoNum:
        print("entered ",filecount)
        break
    print("filecount",filecount)
# conn.close()

print('Count ', count)
print(os.path.getsize('f1.mp4'))