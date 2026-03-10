"""
Test picamera2 and opencv to read QR codes
"""


from picamera2 import Picamera2
import time
import cv2

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

try:
    while True:
        # Capture frame-by-frame
        
        im = picam2.capture_array()
        tm.show('    ')

        qcd = cv2.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(im)
        if retval:
            #cv2.imwrite('output.jpg', im)
            print(retval, decoded_info)
            try:
                code = str(int(decoded_info[0]))
            except ValueError:
                code = 'E   '
            tm.show(code)

        else:
            print(im.shape)
            

            tm.show('----')


except KeyboardInterrupt:
    print("Interrupted!")
    
finally:
    # Clean up
    picam2.stop()
    cv2.destroyAllWindows()
    print("Done!")



# Gives error: Library QUIRC is not linked. No decoding is performed. Take it to the OpenCV repository.