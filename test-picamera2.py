"""
Test picamera2 and opencv to read QR codes
"""


from picamera2 import Picamera2
import time
import numpy as np

print(np.__version__)



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
        print(im.shape)

        time.sleep(1)
        

except KeyboardInterrupt:
    print("Interrupted!")
    
finally:
    # Clean up
    picam2.stop()
    print("Done!")



# Gives error: Library QUIRC is not linked. No decoding is performed. Take it to the OpenCV repository.