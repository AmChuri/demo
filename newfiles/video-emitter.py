import socket  # Import socket module
import os
import time






port = 60000  # Reserve a port for your service every new transfer wants a new port or you must wait.
# s = socket.socket()  # Create a socket object
host = '127.0.0.1'  # Get local machine name
# s.bind((host, port))  # Bind to the port

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
count = 1;
filecount = 0
videoNum = 100
byteRead = 2064 #total number of bytes read/send per transfer

# print(os.path.getsize('/home/amey/anaconda3/envs/pishang/newfiles/new6.mp4'))
starttime = time.time()

# We'll limit ourself to a 40KB/sec maximum send rate
maxSendRateBytesPerSecond = (videoNum*byteRead)

def ConvertSecondsToBytes(numSeconds):
   return numSeconds*maxSendRateBytesPerSecond


def ConvertBytesToSeconds(numBytes):
   return float(numBytes)/maxSendRateBytesPerSecond


# We'll add to this tally as we send() bytes, and subtract from
# at the schedule specified by (maxSendRateBytesPerSecond)
bytesAheadOfSchedule = 0

# Dummy data buffer, just for testing
dataBuf = bytearray(byteRead)

prevTime = None


while True:

    # s.listen(5)  # Now wait for client connection.
    # print('Server listening....')
    # conn, addr = s.accept()  # Establish connection with client.
    # print('Got connection from', addr)

    now = time.time()
    if (prevTime != None):
        bytesAheadOfSchedule -= ConvertSecondsToBytes(now - prevTime)
    prevTime = now

    filename = '/home/amey/anaconda3/envs/pishang/newfiles/new3.ts'  # In the same folder or path is this file running must the file you want to tranfser to be
    # print('filename ',filename)
    # filename = 'data/a.mp4'
    f = open(filename, 'rb')
    l = f.read(byteRead)

    start = time.time()

    # while (l):
    #     count += 1
    #     numBytesSent = l
    #     s.sendto(l, (host, port))
    #     l = f.read(byteRead)
    # f.close()

    s.sendto(l, (host, port))
    numBytesSent = byteRead
    print(numBytesSent)
    if (numBytesSent > 0):
        bytesAheadOfSchedule += numBytesSent
        if (bytesAheadOfSchedule > 0):
            time.sleep(ConvertBytesToSeconds(bytesAheadOfSchedule))
    else:
        print
        "Error sending data, exiting!"
        break
    # s.sendto(b'END', (host, port))  # send empty byte to inform about closing file
    filecount +=1


    if filecount == videoNum:
        print("entered ",filecount)
        break
    print("filecount",filecount)
# conn.close()

print('Count ', count)
# print(os.path.getsize('f1.mp4'))
print(time.time()-starttime)

x = 0
while(x<11):
    s.sendto(b'END', (host, port))
    x+=1