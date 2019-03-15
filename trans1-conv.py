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

cmd = 'ps -p '+str(pid)+' -o %cpu'
ramcmd = 'ps -p '+str(pid)+' -o %mem'
os.system(cmd)

while True:
    filename = 'data/result/t'+str(count)+'.mp4'
    newfilename = 'data/result/t'+str(count)+'.ts'
    check = os.path.isfile(filename)
    if check:
        fileinfo = os.stat(filename)
        # print("filecount ",filecount)
        if (fileinfo.st_size != 0):
            count += 1
            ff = FFmpeg(
                inputs={filename: None},
                outputs={newfilename: ' -vcodec mpeg2video -acodec mp2 -b:v 1k -b:a 56k -muxrate 1k -f mpegts'}
                    )
            print(ff)
            try:
                ff.run()
            except Exception:
                print('exception for ',count)
                pass

            os.remove(filename)
            val = subprocess.check_output(cmd, shell=True);
            strval = val.decode('ASCII')
            strval = strval.replace('%CPU', '')
            print("strval ", strval)
            process = psutil.Process(pid)
            print(process.memory_info().rss)  # in bytes
            print(os.system(ramcmd))
    if (count == 200):
        break



logging.debug('Exiting convertFiles')