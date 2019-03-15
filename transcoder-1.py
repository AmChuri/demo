import socket                   # Import socket module
import os
import logging
import threading
import time
import subprocess
# import matplotlib.pyplot as plt
from ffmpy import FFmpeg
import csv

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
port = 60000  # Reserve a port for your service every new transfer wants a new port or you must wait.
host = '127.0.0.1'  # Get local machine name


print("Transcoder 1 Program id ",os.getpid())
pid = os.getpid()

cmd = 'ps -p '+str(pid)+' -o %cpu'
os.system(cmd)
totalsum = 0.0 # to store cpu usage to get avg val
avgTime = 0.0
packetarrival_time= []
cpu_usage = []
stopcount = 0
flag = True #how long to run the stats file

videoNum = 121 #number of videos - 1
listVid = {} #list of videos processed and
byteRead = 3072 #total number of bytes read/send per transfer
flagone = False
flagtwo_filecount = 0
# this function gets files from video emitter
def getFiles():
    logging.debug('Starting getFiles')

    host = '127.0.0.1'  #Ip address that the TCPServer  is there
    port = 50000                     # Reserve a port for your service every new transfer wants a new port or you must wait.
    print(host,port)
    count = 1
    filecount = 1
    global stopcount
    global  flagone,flagtwo_filecount
    s_inner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_inner.bind((host, port))
    while True:

        filename = 'data/result/t' + str(filecount) + '.mp4'
        with open(filename, 'wb') as f:
            # print ('file opened')
            count +=1
            data = s_inner.recv(byteRead)


                # write data to a file
            f.write(data)
            f.close()
        print(count)
        fileinfo = os.stat(filename)
        # print("filecount ",filecount)
        if(fileinfo.st_size!=0):
            flagtwo_filecount = filecount
            listVid[filecount]={}
            listVid[filecount]['name'] = ('data/result/t' + str(filecount))
            listVid[filecount]['encoded'] = (False)
            listVid[filecount]['transferReady'] = (False)

            filecount +=1
        else:
            stopcount +=1
        # s_inner.close()
        if filecount == 200:
            flagone = True
            flagtwo_filecount = count
            print("entered ",filecount)
            break
    # print('Successfully got the file')

    print('getfiles connection closed')
    print('Count ',count)

    logging.debug('Exiting getFiles')

#convert files to ts file type
def convertFiles():
    logging.debug('Starting convertFiles')
    count = 0 #count to check if listvid has been updated
    global flagtwo_filecount
    while True:
        if len(listVid)>count:
            if listVid[count+1]['encoded'] == False:
                count +=1
                ff = FFmpeg(
                    inputs={str(listVid[count]['name'])+'.mp4': None},
                    outputs={str(listVid[count]['name'])+'.ts': ' -vcodec mpeg2video -acodec mp2 -b:v 1k -b:a 56k -muxrate 1k -f mpegts'}
                )
                print(ff)
                ff.run()
                listVid[count]['encoded'] = (True)
                listVid[count]['transferReady'] = (True)
                print(listVid[count]['name'])
                os.remove(listVid[count]['name']+".mp4")
        if(count==(flagtwo_filecount-1)):
            break

    logging.debug('Exiting convertFiles')



#send converted ts files to transcoder2
def sendFiles():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    global flag,flagtwo_filecount
    count = 1;
    filecount = 1
    logging.debug('Starting sending Files')
    videocount = 0  # count to check if listvid has been updated
    while True:


        if len(listVid)>videocount:
            print("Transfer ",len(listVid))
            if listVid[videocount+1]['transferReady'] == True:
                print("Transfering file ", listVid[videocount+1])
                videocount += 1
                filename = str(listVid[videocount]['name'])+ '.ts'  # In the same folder or path is this file running must the file you want to tranfser to be

                print('filename ', filename)
                f = open(filename, 'rb')
                l = f.read(byteRead)
                while (l):
                    count += 1
                    conn.send(l)
                    # print('Sent ',repr(l))
                    l = f.read(byteRead)
                f.close()
                filecount += 1
                print('Done sending file ',filename)
        print("exited")
        conn.close()
        if filecount == flagtwo_filecount:
            print("send entered ", filecount)
            flag = False
            break
        print("filecount", filecount)



def collectStats(totalsum=0):
    start = time.time()
    currenttime = time.time()
    innercount = 0
    global flag
    while flag:
        if time.time() - currenttime > 1:
            val = subprocess.check_output(cmd, shell=True);
            strval = val.decode('ASCII')
            strval = strval.replace('%CPU', '')
            print("strval ",strval)
            packetarrival_time.append(time.time() - start)
            cpu_usage.append(strval)
            totalsum += float(strval)
            currenttime = time.time()
            innercount+=1
        if flag == False:
            endtime = time.time()
            break
    print("cpu usage count ",len(cpu_usage))
    print("Avg Cpu usage server ","%.2f" % round(totalsum/innercount,2))
    print(endtime - start)
    wtr = csv.writer(open('cpu_transcoder1_out.csv', 'w'), delimiter=',', lineterminator='\n')
    for x in cpu_usage: wtr.writerow([x])
    wtr = csv.writer(open('cpu_transcoder1_out_time.csv', 'w'), delimiter=',', lineterminator='\n')
    for x in packetarrival_time: wtr.writerow([x])


gf = threading.Thread(name='getFiles', target=getFiles)
cf = threading.Thread(name='convertFiles', target=convertFiles)
sf = threading.Thread(name='sendFiles', target=sendFiles)
cs = threading.Thread(name='collectStats', target=collectStats)

gf.start()
# cf.start()
# sf.start()
# cs.start()