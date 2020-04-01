import bluetooth
from bluetooth.ble import DiscoveryService

import time
import json

# TODO: stub
# Return the number of minutes the dip switch is set to
def readToleranceSetting():
    return 15

# TODO: stub
# Trip the relay in case a malicious device may be present
def sendNotification():
    print('hmmmmmmm maybe bad???')

# Read GPIO dip switch for time setting
limit = readToleranceSetting() / 15

# Scan for bluetooth devices
bt_devices = bluetooth.discover_devices()
ble_devices = DiscoveryService().discover(2)
devices = { **bt_devices, **ble_devices }

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
