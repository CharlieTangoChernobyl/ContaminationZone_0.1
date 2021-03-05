#!/usr/bin/env python

from gpiozero import Button
from signal import pause
import subprocess

def longpress():
    subprocess.call(['shutdown', '-h', 'now'], shell=False)

button = Button(24, hold_time=2)
button.when_held = longpress
pause()
