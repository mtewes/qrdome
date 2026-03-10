"""
Test picamera2 and opencv to read QR codes
"""


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
#config = picam2.create_still_configuration()
#picam2.configure(config)

# Start the camera and capture
picam2.start()
time.sleep(2)  # Wait for settings to take effect


imgdir = Path('/home/mtewes/qrdome_images')
imgdir.mkdir(exist_ok=True)

def save_image(im, code):
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
        i = (i + 1) % 10
    
        # Capture frame-by-frame
        
        im = picam2.capture_array()
        print(im.shape)

        tm.show('    ') # So that it blinks

        qcd = cv2.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(im)
        if retval:
            try:
                code = str(int(decoded_info[0]))
            except ValueError:
                code = 'E   '

            if i == 0: # We save that image
                save_image(im, code)

            print(retval, decoded_info)
            
            tm.show(code)

        else:
            
            tm.show('----')


except KeyboardInterrupt:
    print("Interrupted!")
    
finally:
    # Clean up
    picam2.stop()
    cv2.destroyAllWindows()
    print("Done!")



# Gives error: Library QUIRC is not linked. No decoding is performed. Take it to the OpenCV repository.