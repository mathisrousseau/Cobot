import numpy as np
import cv2
import socket
import math
import struct
import time
import helpers.logger
import tcp.data_transfer

LOG_INTERVAL = 10

X_RES = 640
Y_RES = 480
FPS = 10
JPEG_QUALITY = 75
PICAMERA = True

HOST = "127.0.0.1"
PORT = 3001
ADDRESS = (HOST, PORT)

TIME_BETWEEN_FRAMES = float(1.0 / FPS)

cap = cv2.VideoCapture(0)
#ret = cap.set(3, X_RES)
#ret = cap.set(4, Y_RES)
#print("x res: " + str(cap.get(3)))
#print("y res: " + str(cap.get(4)))

# allow the camera to warmup
time.sleep(0.1)

print("FPS: " + str(FPS))
print("JPEG_QUALITY: " + str(JPEG_QUALITY))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(ADDRESS)

lastLogTime = time.time()

      
while(True):
    try:
        before = time.time()
        # Capture frame-by-frame
        
        ret, frame = cap.read()
        
        if ret:
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Webcam",gray)

            #We need this if we want to display frames on the screen
            k = cv2.waitKey(30) & 0xff
            if k == ord('q'):
                break

            ret, buf = cv2.imencode('.jpeg', gray, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
            #ret, buf = cv2.imencode('.png', gray)
    
            if ret == True:
                npString = str(buf)
                tcp.data_transfer.send_dataset(sock, npString)
            else:
                print('ret == False')
        
            after = time.time()
        
            logDiffTime = after - lastLogTime
            if logDiffTime > LOG_INTERVAL:
                lastLogTime = after
                print('logging')
                after = time.time()
        
            diffTime = after - before
            sleepTime = TIME_BETWEEN_FRAMES - diffTime
            if sleepTime > 0:
                time.sleep(sleepTime)
        
    except socket.error as exc:
        print ("Caught exception socket.error : {}".format(exc))
        break


# When everything done, release the capture
print("closing socket")
sock.close()
cap.release()
