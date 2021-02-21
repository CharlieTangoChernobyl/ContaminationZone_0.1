# THE GEIGER COUNTER (at last)

import time
import datetime
import sys, getopt, os
import RPi.GPIO as GPIO
from collections import deque
from influxdb import InfluxDBClient
from pijuice import PiJuice
from balena import Balena
from twilio.rest import Client
import I2C_LCD_driver

GPIO.setmode(GPIO.BOARD)

counts = deque()
usvh_ratio = 0.00812037037037 # This is for the J305 tube

lcd = I2C_LCD_driver.lcd()
screen_columns = 20
screen_rows = 4

# Start the SDK
balena = Balena()
balena.auth.login_with_token(os.environ['BALENA_API_KEY'])

# Wait for device I2C device to start
while not os.path.exists('/dev/i2c-1'):
    print ("Waiting to identify PiJuice")
    time.sleep(0.1)

# Initiate PiJuice
pijuice = PiJuice(1,0x14)

# Get all parameters and return as a dictionary
def get_battery_paremeters(pijuice):

    juice = {}

    charge = pijuice.status.GetChargeLevel()
    juice['charge'] = charge['data'] if charge['error'] == 'NO_ERROR' else charge['error']

    # Temperature [C]
    temperature =  pijuice.status.GetBatteryTemperature()
    juice['temperature'] = temperature['data'] if temperature['error'] == 'NO_ERROR' else temperature['error']

    # Battery voltage  [V]
    vbat = pijuice.status.GetBatteryVoltage()
    juice['vbat'] = vbat['data']/1000 if vbat['error'] == 'NO_ERROR' else vbat['error']

    # Barrery current [A]
    ibat = pijuice.status.GetBatteryCurrent()
    juice['ibat'] = ibat['data']/1000 if ibat['error'] == 'NO_ERROR' else ibat['error']

    # I/O coltage [V]
    vio =  pijuice.status.GetIoVoltage()
    juice['vio'] = vio['data']/1000 if vio['error'] == 'NO_ERROR' else vio['error']

    # I/O current [A]
    iio = pijuice.status.GetIoCurrent()
    juice['iio'] = iio['data']/1000 if iio['error'] == 'NO_ERROR' else iio['error']

    # Get power input (if power connected to the PiJuice board)
    status = pijuice.status.GetStatus()
    juice['power_input'] = status['data']['powerInput'] if status['error'] == 'NO_ERROR' else status['error']

    # Get power input (if power connected to the Raspberry Pi board)
    status = pijuice.status.GetStatus()
    juice['power_input_board'] = status['data']['powerInput5vIo'] if status['error'] == 'NO_ERROR' else status['error']

    return juice

def update_tag(tag, variable):
    # update device tags
    balena.models.tag.device.set(os.environ['BALENA_DEVICE_UUID'], str(tag), str(variable))

# Change start tag
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
update_tag("START_TIME", start_time)

# Initial variables
i = 0

while True:

    #Read battery data
    battery_data = get_battery_paremeters(pijuice)
    # Uncomment the line to display battery status on long
    # print(battery_data)

    # Change tags every minute
    if(i%12==0):
        # Update tags
        for key, value in battery_data.items():
            update_tag(key, value)

    i = i + 1
    sleep(5)


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
