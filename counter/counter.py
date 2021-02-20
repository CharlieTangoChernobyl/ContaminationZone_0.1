# THE GEIGER COUNTER (at last)

import time
import datetime
import RPi.GPIO as GPIO
from collections import deque
from influxdb import InfluxDBClient
import I2C_LCD_driver

counts = deque()
hundredcount = 0
usvh_ratio = 0.00812037037037 # This is for the J305 tube

lcd = I2C_LCD_driver.lcd()
screen_columns = 20
screen_rows = 4

lcd.lcd_display_string("Hello Cunt", 1, 0)
lcd.lcd_display_string("Line 2", 2, 0)
lcd.lcd_display_string("Line 3", 3, 0)
lcd.lcd_display_string("Line 4", 4, 0)

# This method fires on edge detection (the pulse from the counter board)
def countme(channel):
    global counts, hundredcount
    timestamp = datetime.datetime.now()
    counts.append(timestamp)

    # Every time we hit 100 counts, run count100 and reset
    hundredcount = hundredcount + 1
    if hundredcount >= 100:
        hundredcount = 0
        count100()

# This method runs the servo to increment the mechanical counter
def count100():
    GPIO.setup(12, GPIO.OUT)
    pwm = GPIO.PWM(12, 50)

    pwm.start(4)
    time.sleep(1)
    pwm.start(9.5)
    time.sleep(1)
    pwm.stop()


# Set the input with falling edge detection for geiger counter pulses
GPIO.setup(16, GPIO.IN)
GPIO.add_event_detect(16, GPIO.FALLING, callback=countme)

# Setup influx client (this is using a modified version of balenaSense)
influx_client = InfluxDBClient('influxdb', 8086, database='balena-sense')
influx_client.create_database('balena-sense')

loop_count = 0

# In order to calculate CPM we need to store a rolling count of events in the last 60 seconds
# This loop runs every second to update the Nixie display and removes elements from the queue
# that are older than 60 seconds
while True:
    loop_count = loop_count + 1
        
    try:
        while counts[0] < datetime.datetime.now() - datetime.timedelta(seconds=60):
            counts.popleft()
    except IndexError:
        pass # there are no records in the queue.
    
    if loop_count == 10:
        # Every 10th iteration (10 seconds), store a measurement in Influx
        measurements = [
            {
                'measurement': 'balena-sense',
                'fields': {
                    'cpm': int(len(counts)),
                    'usvh': "{:.2f}".format(len(counts)*usvh_ratio)
                }
            }
        ]
        
        influx_client.write_points(measurements)
        loop_count = 0
    
    # Update the displays with a zero-padded string

    
    time.sleep(1)