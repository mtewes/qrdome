"""
Test picamera2 and opencv to read QR codes

Doc:
https://www.raspberrypi.com/documentation/computers/camera_software.html#picamera2
https://docs.opencv.org/3.4/de/dc3/classcv_1_1QRCodeDetector.html


[{'bit_depth': 10,
  'crop_limits': (16, 0, 2560, 1920),
  'exposure_limits': (134, 4879289, 20000),
  'format': SGBRG10_CSI2P,
  'fps': 58.92,
  'size': (640, 480),
  'unpacked': 'SGBRG10'},
 {'bit_depth': 10,
  'crop_limits': (0, 0, 2592, 1944),
  'exposure_limits': (86, 3066985, 20000),
  'format': SGBRG10_CSI2P,
  'fps': 46.34,
  'size': (1296, 972),
  'unpacked': 'SGBRG10'},
 {'bit_depth': 10,
  'crop_limits': (348, 434, 1928, 1080),
  'exposure_limits': (110, 3066979, 20000),
  'format': SGBRG10_CSI2P,
  'fps': 32.81,
  'size': (1920, 1080),
  'unpacked': 'SGBRG10'},
 {'bit_depth': 10,
  'crop_limits': (0, 0, 2592, 1944),
  'exposure_limits': (130, 3066985, 20000),
  'format': SGBRG10_CSI2P,
  'fps': 15.63,
  'size': (2592, 1944),
  'unpacked': 'SGBRG10'}]

"""

#from pprint import *
from picamera2 import Picamera2

import time
import cv2
import datetime
from pathlib import Path

import tm1637

print("OpenCV version: ", cv2.__version__)

# Start display
CLK = 6
DIO = 5
tm = tm1637.TM1637(clk=CLK, dio=DIO)
tm.brightness(2)
tm.show('S---')


# Initialize Picamera2 and configure the camera
picam2 = Picamera2()

#pprint(picam2.sensor_modes)

#preview_config = picam2.create_preview_configuration()
#config = picam2.create_still_configuration()
#picam2.configure(preview_config)
picam2.configure()

# Start the camera and capture
picam2.start()
time.sleep(2)  # Wait for settings to take effect


imgdir = Path('/home/mtewes/qrdome_images')
imgdir.mkdir(exist_ok=True)

def save_image(im, code):
    if True:
        # First we create a directory for today's date
        today = datetime.date.today().isoformat()
        d = imgdir / today
        d.mkdir(exist_ok=True)
        # Then we save the image with a timestamp
        timestamp = datetime.datetime.now().strftime("%H-%M-%S-%f")
        output_path = d / f'{timestamp}_code_{code.strip(" ")}.jpg'
        cv2.imwrite(str(output_path), im)
        print(f"Saved image to {output_path}")


try:
    i = 0
    while True:
        i = i % 20
    
        # Capture frame-by-frame
        
        im = picam2.capture_array()
        print(im.shape)

        tm.show('    ') # Clear display, so that it blinks

        qcd = cv2.QRCodeDetector()
        #retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(im)
        #decoded_info = decoded_info[0] # We pick the first in case of multi
        #if retval:
        #    try:
        #        code = str(int(decoded_info))
        #    except ValueError:
        #        code = 'E   '

        data, points, straight_qrcode = qcd.detectAndDecode(im)
        if data: # if this string is not empty...
            try:
                code = str(int(data))
            except ValueError:
                code = 'E   '
            
            print(data) 
            tm.show(code)

            save_image(im, code)

        else:
            
            tm.show('----')

            if i == 0: # We save that image
                save_image(im, "N")

        
        i=i+1
            
            


except KeyboardInterrupt:
    print("Interrupted!")
    
finally:
    # Clean up
    picam2.stop()
    cv2.destroyAllWindows()
    print("Done!")

