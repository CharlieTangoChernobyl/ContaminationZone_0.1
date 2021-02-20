# THE GEIGER COUNTER (at last)

import time
import datetime
import RPi.GPIO as GPIO
from collections import deque
from influxdb import InfluxDBClient
import I2C_LCD_driver

GPIO.setmode(GPIO.BOARD)

counts = deque()
usvh_ratio = 0.00812037037037 # This is for the J305 tube

lcd = I2C_LCD_driver.lcd()
screen_columns = 20
screen_rows = 4

# This method fires on edge detection (the pulse from the counter board)
def countme(channel):
    global counts
    timestamp = datetime.datetime.now()
    counts.append(timestamp)


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
    
    # Update the displays
    line1 = "uSv/h: {:.2f}   ".format(len(counts)*usvh_ratio)
    line2 = "CPM: {}    ".format(int(len(counts)))
    line3 = "   contamination    "
    line4 = "      zone.net      "

    lcd.lcd_display_string(line1, 1, 0)
    lcd.lcd_display_string(line2, 2, 0)
    lcd.lcd_display_string(line3, 3, 0)
    lcd.lcd_display_string(line4, 4, 0)
    
    time.sleep(1)