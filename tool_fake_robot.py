import time
import socket
import helpers.logger
import datagram.image_reader
import processing.face_detector

#Constants

ADDRESS = ('127.0.0.1', 3000)

LOG_INTERVAL = 10

OK = 'OK'

info_logger = helpers.logger.setup_normal_logger('Fake_Robot')
    
if __name__ == "__main__":

    # Create the server, binding to localhost
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Disable Nagle's algorithm
    # This should not be active since the robot probably doesn't support this
    # sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    
    sock.settimeout(10)
    sock.connect(ADDRESS)
    
    while True:
        try:
            # Send data
            sock.send(OK.encode())
            #print("The message is sent")
            data = sock.recv(1024).strip().decode()
            info_logger.info('received "{}"'.format(data))
            print ('received "{}"'.format(data))
            time.sleep(0.2)

        #In python2, we use "," and in python3 it is "as"
        except socket.error as exc:
            print ("Caught exception socket.error : {}".format(exc))
            break
    
    #End While
    print('closing socket')
    sock.close()
    
    print('exiting')
