import socket                   # Import socket module
import os
import logging
import threading
import time
import subprocess
from ffmpy import FFmpeg
import csv

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

port = 20000  # Reserve a port for your service every new transfer wants a new port or you must wait.
# s = socket.socket()  # Create a socket object
host = "127.0.0.1"  # Get local machine name
# s.bind((host, port))  # Bind to the port

print("Transcoder 1 Program id ",os.getpid())
pid = os.getpid()

cmd = 'ps -p '+str(pid)+' -o %cpu'
os.system(cmd)
totalsum = 0.0 # to store cpu usage to get avg val
avgTime = 0.0
packetarrival_time= []
cpu_usage = []

flag = True #how long to run the stats file

videoNum = 121 #number of videos - 1
listVid = {} #list of videos processed and
byteRead = 2064 #total number of bytes read/send per transfer
# this function gets files from video emitter

latency = []
exitflag = False
def getFiles():

    logging.debug('Starting getFiles')

    host = '127.0.0.1'  #Ip address that the TCPServer  is there
    port = 60000                     # Reserve a port for your service every new transfer wants a new port or you must wait.
    print(host,port)
    count = 0
    filecount = 1
    global stopcount, exitflag
    global  flagone,flagtwo_filecount
    s_inner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_inner.bind((host, port))
    print(len(latency))
    while True:

        filename = 'data/result/con' + str(filecount) + '.ts'
        data = s_inner.recv(byteRead)
        if (len(data) == 3):
            exitflag = True
            f = open(filename, "wb")
            f.close()
            break
        with open(filename, 'wb') as f:
            # print ('file opened')
            count +=1
            arrival_time = time.time()

            f.write(data)
            f.close()
        print(count)
        if exitflag:
            break
        fileinfo = os.stat(filename)
        # print("filecount ",filecount)
        if(fileinfo.st_size!=0):
            flagtwo_filecount = filecount
            listVid[filecount]={}
            listVid[filecount]['name'] = ('data/result/con' + str(filecount))
            listVid[filecount]['encoded'] = (False)
            listVid[filecount]['transferReady'] = (False)
            departure_time = time.time()

            filecount +=1
        else:
            stopcount +=1
        latency.append(departure_time-arrival_time)
        # s_inner.close()
        # if filecount == 110:
        #     flagone = True
        #     flagtwo_filecount = count
        #     print("entered ",filecount)
        #     break
    # print('Successfully got the file')

    print('getfiles connection closed')
    print('Count ',count)

    wtr = csv.writer(open('latency_arrive.csv', 'w'), delimiter=',', lineterminator='\n')
    for x in latency: wtr.writerow([x])
    logging.debug('Exiting getFiles')
# print(os.path.getsize('t.mp4'))


cf = threading.Thread(name='getFiles', target=getFiles)


cf.start()
# gf.start()
# sf.start()
# cs.start()