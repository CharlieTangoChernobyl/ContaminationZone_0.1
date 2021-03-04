#!/usr/bin/env python3
#!
import RPi.GPIO as GPIO
import time
import pydbus
import gi

# Set GPIO mode: GPIO.BCM or GPIO.BOARD
GPIO.setmode(GPIO.BOARD)

# Set pin 5 an an input, and enable the internal pull-up resistor
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

oldButtonState1 = True

while True:
    buttonState1 = GPIO.input(7)

    if buttonState1 != oldButtonState1 and buttonState1 == False :
        bus = pydbus.SystemBus()
        logind = bus.get('.login1')['.Manager']
        logind.PowerOff(True)

    oldButtonState1 = buttonState1

time.sleep(1)
