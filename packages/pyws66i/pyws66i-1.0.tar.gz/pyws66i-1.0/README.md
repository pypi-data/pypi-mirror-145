## Status
[![Build Status](https://app.travis-ci.com/ssaenger/pyws66i.svg?branch=master)](https://app.travis-ci.com/ssaenger/pyws66i)[![Coverage Status](https://coveralls.io/repos/github/ssaenger/pyws66i/badge.svg?branch=master)](https://coveralls.io/github/ssaenger/pyws66i?branch=master)

# pyws66i
Python3 interface implementation for [Soundavo WS66i amplifier](https://www.soundavo.com/products/ws-66i).

## Notes
This is a 6-zone amplifier that is a direct upgrade from ws66i 6-zone amplifier. This is a fork off of [pymonoprice](https://github.com/etsinko/pymonoprice) that replaces the serial protocol for telnet.

It is intended to be used with [Home-Assistant](http://home-assistant.io).

## Usage
```python
from pyws66i import get_ws66i

# Get a connection using the IP address of the WS66i amplifier
ws66i = get_ws66i('192.168.1.123')

# Open a connection
try:
    ws66i.open()
except ConnectionError:
    # Handle exception

# Valid zones are 11-16 for the main WS66i amplifier
zone_status = ws66i.zone_status(11)

# Print zone status
print('Zone Number = {}'.format(zone_status.zone))
print('Power is {}'.format('On' if zone_status.power else 'Off'))
print('Mute is {}'.format('On' if zone_status.mute else 'Off'))
print('Public Anouncement Mode is {}'.format('On' if zone_status.pa else 'Off'))
print('Do Not Disturb Mode is {}'.format('On' if zone_status.do_not_disturb else 'Off'))
print('Volume = {}'.format(zone_status.volume))
print('Treble = {}'.format(zone_status.treble))
print('Bass = {}'.format(zone_status.bass))
print('Balance = {}'.format(zone_status.balance))
print('Source = {}'.format(zone_status.source))
print('Keypad is {}'.format('connected' if zone_status.keypad else 'disconnected'))

# Turn off zone #11
ws66i.set_power(11, False)

# Mute zone #12
ws66i.set_mute(12, True)

# Set volume for zone #13
ws66i.set_volume(13, 15)

# Set source 1 for zone #14
ws66i.set_source(14, 1)

# Set treble for zone #15
ws66i.set_treble(15, 10)

# Set bass for zone #16
ws66i.set_bass(16, 7)

# Set balance for zone #11
ws66i.set_balance(11, 3)

# Restore zone #11 to it's original state
ws66i.restore_zone(zone_status)

# Done. Close the connection
ws66i.close()
```
