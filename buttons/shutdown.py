# THE GEIGER COUNTER (at last)

import time
import datetime
import RPi.GPIO as GPIO
import smbus

GPIO.setmode(GPIO.BOARD)

# This method fires on edge detection (the pulse from the counter board)
def countme(channel):
    os.system('shutdown -h now')

# Set the input with falling edge detection for geiger counter pulses
GPIO.setup(37, GPIO.IN)
GPIO.add_event_detect(37, GPIO.FALLING, callback=countme)