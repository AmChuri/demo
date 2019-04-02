import socket                   # Import socket module
import os
import logging
import threading
import time
import subprocess
# import matplotlib.pyplot as plt
from ffmpy import FFmpeg
import csv


videoNum = 200 #number of videos - 1
listVid = {} #list of videos processed and
byteRead = 3072 #total number of bytes read/send per transfer

host = "127.0.0.1"  # Ip address that the TCPServer  is there
port = 20000  # Reserve a port for your service every new transfer wants a new port or you must wait.

count = 1
filecount = 1

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a socket object
s.connect((host, port))

while True:
    filename = 'data/result/final' + str(filecount) + '.mp4'
    timedif = time.time()
    with open(filename, 'wb') as f:
        # print ('file opened')
        count +=1
        data = s.recv(byteRead)
        print(data)

        # write data to a file
        f.write(data)
        f.close()
    print(count)
    fileinfo = os.stat(filename)
    if (fileinfo.st_size != 0):
        filecount += 1
        print("filecount ",filecount)

    if filecount == videoNum:
        # print("entered ",filecount)
        break
print('Successfully got the file')

print('connection closed')
print('Count ',count)