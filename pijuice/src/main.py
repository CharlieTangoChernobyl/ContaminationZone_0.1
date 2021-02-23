from time import sleep
import datetime
import sys
import getopt
import os
from pijuice import PiJuice
from balena import Balena
from twilio.rest import Client
import counter.py

# Start the SDK
balena = Balena()
balena.auth.login_with_token(os.environ['BALENA_API_KEY'])

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
