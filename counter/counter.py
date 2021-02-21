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

#some parts do not need to update every second
line1 = "uSv/h: "
line2 = "CPM: "
line3 = " System starting..."
lcd.lcd_display_string(line1, 1, 0)
lcd.lcd_display_string(line2, 2, 0)
lcd.lcd_display_string(line3, 3, 0)

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
    line1 = "{:.2f}   ".format(len(counts)*usvh_ratio)
    line2 = "{}    ".format(int(len(counts)))

    lcd.lcd_display_string(line4, 4, 8)
    lcd.lcd_display_string(line2, 2, 6)
    
    time.sleep(1)

line4 = "0%"
lcd.lcd_display_string(line4, 1, 9)
time.sleep(0.6)
line4 = "1%"
lcd.lcd_display_string(line4, 1, 9)
time.sleep(0.6)
line4 = "2%"
lcd.lcd_display_string(line4, 1, 9)
time.sleep(0.6)
line4 = "3%"
lcd.lcd_display_string(line4, 1, 9)
time.sleep(0.6)
line4 = "4%"
lcd.lcd_display_string(line4, 1, 9)
time.sleep(0.6)
line4 = "5%"
lcd.lcd_display_string(line4, 1, 9)
time.sleep(0.6)
line4 = "6%"
lcd.lcd_display_string(line4, 1, 9)
time.sleep(0.6)
line4 = "7%"
lcd.lcd_display_string(line4, 1, 9)
time.sleep(0.6)
line4 = "8%"
lcd.lcd_display_string(line4, 1, 9)
time.sleep(0.6)
line4 = "9%"
lcd.lcd_display_string(line4, 1, 9)
time.sleep(0.6)
line4 = "10%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "11%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "12%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "13%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "14%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "15%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "16%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "17%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "18%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "19%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "20%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "21%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "22%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "23%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "24%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "25%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "26%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "27%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "28%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "29%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "30%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "31%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "32%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "33%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "34%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "35%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "36%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "37%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "38%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "39%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "40%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "41%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "42%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "43%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "44%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "45%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "46%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "47%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "48%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "49%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "50%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "51%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "52%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "53%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "54%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "55%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "56%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "57%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "58%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "59%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "60%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "61%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "62%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "63%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "64%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "65%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "66%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "67%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "68%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "69%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "70%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "71%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "72%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "73%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "74%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "75%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "76%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "77%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "78%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "79%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "80%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "81%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "82%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "83%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "84%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "85%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "86%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "87%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "88%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "89%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "90%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "91%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "92%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "93%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "94%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "95%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "96%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "97%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "98%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "99%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line4 = "100%"
lcd.lcd_display_string(line4, 4, 8)
time.sleep(0.6)
line3 = "contamination"
line4 = "zone.net"
lcd.lcd_display_string(line3, 3, 5)
lcd.lcd_display_string(line4, 4, 6)
