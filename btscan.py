import bluetooth
import time
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
GPIO.setup(33, GPIO.IN)
GPIO.setup(35, GPIO.IN)
GPIO.setup(37, GPIO.IN)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.output(23, GPIO.LOW)
GPIO.output(21, GPIO.LOW)

# TODO: stub
# Return the number of minutes the dip switch is set to
def readToleranceSetting():
  return 15
  # input1 = GPIO.input(33)
  # input2 = GPIO.input(35)
  # input3 = GPIO.input(37)

# TODO: stub
# Trip the relay in case a malicious device may be present
def sendNotification():
  GPIO.output(23, GPIO.HIGH)
  GPIO.output(21, GPIO.HIGH)

# Read GPIO dip switch for time setting
limit = readToleranceSetting() / 15

# Scan for bluetooth devices
devices = bluetooth.discover_devices()

# Record all addresses with a timestamp in CSV format
with open('records.csv', 'a') as records:
  records.write(f'{time.ctime()}')
  for addr in devices:
    records.write(f', {addr}')
  records.write('\n')

# Load the previous list of addresses from JSON
state = json.load('state.json')

# Remove any absent keys from the state
for key, value in state.items():
  if key not in devices:
    del state[key]

# Add each present key to the state, incrementing any old keys
for addr in devices:
  if addr not in state:
    state[addr] = 0
  else:
    state[addr] = state[addr] + 1

# Search for any addresses that've hung around too long
for addr, count in state:
  if count >= limit:
    sendNotification()

# Store the current state in the state FileExistsError
json.dump(state, 'state.json')


#there's two stubs for reading from GPIO and writing to the relay, which I can't do much about without a device handy
#the script is designed to be run periodically by a task runner like cron
#mostly so that I don't have to handle restart logic myself in case the script crashes for whatever reason
#I wouldn't set it to run any less frequently than every 15 minutes
#as indicated, the readToleranceSetting function should return a value in minutes, as determined by the dipswitch value
