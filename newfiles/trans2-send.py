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

port = 20000
host = '127.0.0.1'  # Get local machine name
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
latency = []
exitflag = False


def endprog():
    ef_inner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ef_inner.bind((host, 20001))
    print("HERE")
    newdata = ef_inner.recv(byteRead)
    print(newdata)

ep = threading.Thread(name='endprog', target=endprog)


ep.start()
def sendpack():
    global count

    while True:
        # print("Entered")
        filename = 'data/result/con'+str(count)+'.mp4'
        check = os.path.isfile(filename)
        if check:
            fileinfo = os.stat(filename)
            # print("filecount ",filecount)
            if (fileinfo.st_size != 0):
                if(fileinfo.st_size > 2000):
                    arrival_time = time.time()
                    count+1
                    f = open(filename, 'rb')
                    l = f.read(byteRead)
                    while (l):
                        count += 1
                        # conn.send(l)
                        s.sendto(l, (host, port))
                        l = f.read(byteRead)
                    f.close()
                    departure_time = time.time()
                    latency.append(departure_time - arrival_time)
                else:
                    count+1
                print(count)
        # else:
        #     if count != 1:
        #         exitflag = True
        #         break
        if exitflag:
            break



ep = threading.Thread(name='endprog', target=endprog)
sp = threading.Thread(name='sendpack', target=sendpack)


ep.start()


sp.start()

wtr = csv.writer(open('latency_send.csv', 'w'), delimiter=',', lineterminator='\n')
for x in latency: wtr.writerow([x])
print("Done")