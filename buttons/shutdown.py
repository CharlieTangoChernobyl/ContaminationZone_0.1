# THE GEIGER COUNTER (at last)

import time
import datetime
import RPi.GPIO as GPIO
import smbus

# This method fires on edge detection (the pulse from the counter board)
def countme(channel):
    os.system('shutdown -h now')

# Set the input with falling edge detection for geiger counter pulses
GPIO.setup(26, GPIO.IN)
GPIO.add_event_detect(26, GPIO.FALLING, callback=countme)