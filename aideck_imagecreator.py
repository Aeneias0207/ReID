import time
import socket, struct, time
import numpy as np
import cv2
import threading
import os

IP = '192.168.2.22'
PORT = 5000
DEVICE_NUMBER = 0
WIDTH = 324
HEIGHT = 244
FPS = 20


def colorBalance(img):
    '''
    Function to color balance wrt a white object
    '''
    mean = [0,0,0]
    factor = [1,1,1]
    img_out = img.copy()
    for c in range(3):
        mean[c] = np.mean(img[:,:,c].flatten())
        factor[c] = 255.0/mean[c]
        img_out[:,:,c] = np.clip(img_out[:,:,c]*factor[c],0,255)

    print("Factors: {}".format(factor))
    return img_out, factor

def colorBalanceStretch(img, perc = 0.05):
    '''
    Similar to the above, but only using min and max in the 0.05 percentile.
    '''
    factor = [1,1,1]
    img_out = img.copy()
    for c in range(3):
        mi, ma = (np.percentile(img[:,:,c], perc), np.percentile(img[:,:,c],100.0-perc))
        factor[c] = 255.0/(ma-mi)
        img_out[:,:,c] = np.clip(img_out[:,:,c]*factor[c],0,255)

    print("Factors: {}".format(factor))
    return img_out, factor
    


def colorCorrectBayer(img_, factors=[1,1,1]):
    '''
    Color correction for the RGB Camera. It has a sensor with a Bayer pattern, which has
    more green cells than blue and red, so if the image is not treated, it will have  a
    green-ish look.
    '''
    # TODO: Apply an actual color correction without luminosity loss. -> histogram level
    # This is just an approximation
    img = img_.copy()
    for i in range(3):
        img[:,:,i] = np.clip(img[:,:,i]*factors[i],0,255)
    return img

def rx_bytes(size, client_socket):
    '''
    Read N bytes from the socket
    '''
    data = bytearray()
    while len(data) < size:
        data.extend(client_socket.recv(size-len(data)))
    return data

def safe_create_folder(name):
    if os.path.exists(name):
        return
    else:
        os.mkdir(name)



class Connector(threading.Thread):

    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.factors = [1.8648577393897736, 1.2606252586922309, 1.4528872589128194]

        self.timer_period = 0.1  # seconds
        
        
        # dirname = os.path.dirname(__file__)
        # if not os.path.exists(os.path.join(dirname,'recordings')):
        #     print(os.path.join(dirname,'recordings'))
        #     print(os.path.exists('/home/hendrik/Documents/images/recordings'))
        #     print('cwd(): '+ os.getcwd())
        #     print(os.path.join(os.getcwd(),'recordings'))
        #     print('folder does not exist')
        # else: print('folder exists')
        
        # print("Connecting to socket on {}:{}...".format(IP, PORT))
        # self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.connect((IP, PORT))
        # print("Socket connected")

        # self.cam = pyvirtualcam.Camera(width=WIDTH, height=HEIGHT, fps=FPS, device=f'/dev/video{DEVICE_NUMBER}')
        self.count = 0
        self.img = None
        
        # create recordings folder if not yet existent
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, 'recordings')
        if not os.path.exists(path):
            os.mkdir(path)
            
        self.startTime = time.time()
        safe_create_folder(os.path.join(f"recordings/images_{int(self.startTime)}"))
        self.running = True
        print("Starting recording...")
        self.start()

    def run(self):
        while self.running:
            self.timer_callback()
            time.sleep(self.timer_period)

    def timer_callback(self):
        format, imgs = self.getImage(self.client_socket)

        # if imgs is not None and format == 0:
        #     img = imgs[-1]
        #     img = colorCorrectBayer(img,self.factors)

            # push image to virtual cam
            # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            # self.cam.send(img)

    def getImage(self, client_socket):
        '''
        Function to receive an image from the socket
        '''
        # First get the info
        packetInfoRaw = rx_bytes(4, client_socket)
        #print(packetInfoRaw)
        [length, routing, function] = struct.unpack('<HBB', packetInfoRaw)
        #print("Length is {}".format(length))
        #print("Route is 0x{:02X}->0x{:02X}".format(routing & 0xF, routing >> 4))
        #print("Function is 0x{:02X}".format(function))

        imgHeader = rx_bytes(length - 2, client_socket)
        #print(imgHeader)
        #print("Length of data is {}".format(len(imgHeader)))
        [magic, width, height, depth, format, size] = struct.unpack('<BHHBBI', imgHeader)

        imgs = None
        
        # check if recordings folder exists else create it
        dirname = os.path.dirname(__file__)
        if not os.path.exists(os.path.join(os.getcwd(),'recordings')):
            print('ausgeführt')
            os.mkdir(os.path.join(os.getcwd(),'recordings'))

        if magic == 0xBC:
            #print("Magic is good")
            #print("Resolution is {}x{} with depth of {} byte(s)".format(width, height, depth))
            #print("Image format is {}".format(format))
            #print("Image size is {} bytes".format(size))

            # Now we start rx the image, this will be split up in packages of some size
            imgStream = bytearray()

            while len(imgStream) < size:
                packetInfoRaw = rx_bytes(4, client_socket)
                [length, dst, src] = struct.unpack('<HBB', packetInfoRaw)
                #print("Chunk size is {} ({:02X}->{:02X})".format(length, src, dst))
                chunk = rx_bytes(length - 2, client_socket)
                imgStream.extend(chunk)
            
            self.count = self.count + 1
            meanTimePerImage = (time.time()-self.startTime) / self.count

            # TODO: CHange to debug and rclpy
            # print("{}".format(meanTimePerImage))
            # print("{}".format(1/meanTimePerImage))

            if format == 0:
                bayer_img = np.frombuffer(imgStream, dtype=np.uint8)   
                bayer_img.shape = (244, 324)
                color_img = cv2.cvtColor(bayer_img, cv2.COLOR_BayerBG2BGR)

                k = cv2.waitKey(1)
                if k == ord('b'):
                    _,self.factors = colorBalance(color_img)
                elif k == ord('q'):
                    self.running = False
                
                
                cv2.imshow('Raw', bayer_img)
                cv2.imshow('Color', colorCorrectBayer(color_img,self.factors))
                if k == ord('s'):
                    cv2.imwrite(os.path.join(f"recordings/images_{int(self.startTime)}", f"{self.count}.jpg"), colorCorrectBayer(color_img,self.factors))
                cv2.waitKey(1)
                imgs = [bayer_img,color_img]
            else:
                nparr = np.frombuffer(imgStream, np.uint8)
                decoded = cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED)
                cv2.imshow('JPEG', decoded)
                cv2.waitKey(1)
                imgs = [decoded]

        return format,imgs



if __name__ == '__main__':
    connector = Connector()