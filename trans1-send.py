import socket                   # Import socket module
import os
import logging
import threading
import time
import subprocess
# import matplotlib.pyplot as plt
from ffmpy import FFmpeg
import csv
count = 1
byteRead = 3072 #total number of bytes read/send per transfer

port = 60000
host = '127.0.0.1'  # Get local machine name
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    filename = 'data/result/t'+str(count)+'.ts'
    check = os.path.isfile(filename)
    if check:
        fileinfo = os.stat(filename)
        # print("filecount ",filecount)
        if (fileinfo.st_size != 0):
            if(fileinfo.st_size > 2000):

                count+1
                f = open(filename, 'rb')
                l = f.read(byteRead)
                while (l):
                    count += 1
                    # conn.send(l)
                    s.sendto(l, (host, port))
                    l = f.read(byteRead)
                f.close()
            else:
                count+1
            print(count)
    if count ==200:
        break
print("Done")

