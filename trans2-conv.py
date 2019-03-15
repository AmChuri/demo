import socket                   # Import socket module
import os
import logging
import threading
import time
import subprocess
# import matplotlib.pyplot as plt
from ffmpy import FFmpeg
import csv
import psutil

listVid = {}
count = 1

pid = os.getpid()

print("PID",pid)
totalsum = 0.0 # to store cpu usage to get avg val
avgTime = 0.0
packetarrival_time= []
cpu_usage = []
ram_usage = []
latency = []
cmd = 'ps -p '+str(pid)+' -o %cpu'
ramcmd = 'ps -p '+str(pid)+' -o %mem'
os.system(cmd)
start = time.time()
innercount = 0
while True:
    filename = 'data/result/con'+str(count)+'.ts'
    newfilename = 'data/result/con'+str(count)+'.mp4'
    check = os.path.isfile(filename)
    if check:
        fileinfo = os.stat(filename)
        # print("filecount ",filecount)
        if (fileinfo.st_size != 0):
            arrival_time = time.time()
            count += 1
            ff = FFmpeg(
                inputs={filename: None},
                outputs={newfilename: ' -c copy'}
                    )
            print(ff)
            try:
                ff.run()
            except Exception:
                print('exception for ',count)

                pass
            departure_time = time.time()
            latency.append(departure_time - arrival_time)
            os.remove(filename)
            val = subprocess.check_output(cmd, shell=True);
            strval = val.decode('ASCII')
            strval = strval.replace('%CPU', '')
            print("strval ", strval)
            process = psutil.Process(pid)
            print(process.memory_info().rss)  # in bytes
            print(os.system(ramcmd))

            val = subprocess.check_output(cmd, shell=True);
            strval = val.decode('ASCII')
            strval = strval.replace('%CPU', '')
            print("strval ", strval)
            packetarrival_time.append(time.time() - start)
            cpu_usage.append(strval)
            totalsum += float(strval)
            currenttime = time.time()
            innercount += 1
            currenttime = time.time()
            innercount = 0

    if (count == 200):
        endtime = time.time()
        break
# print("Avg Cpu usage server ","%.2f" % round(totalsum/innercount,2))
print(endtime - start)
wtr = csv.writer(open('cpu_transcoder2_out.csv', 'w'), delimiter=',', lineterminator='\n')
for x in cpu_usage: wtr.writerow([x])
wtr = csv.writer(open('cpu_transcoder2_out_time.csv', 'w'), delimiter=',', lineterminator='\n')
for x in packetarrival_time: wtr.writerow([x])

wtr = csv.writer(open('latency_conv.csv', 'w'), delimiter=',', lineterminator='\n')
for x in latency: wtr.writerow([x])

logging.debug('Exiting convertFiles')