import RPi.GPIO as GPIO
import pywemo
import time
import os

# TODO: Add a blinking LED so I can see at a glance if this script is on or not

# Setup thermostat interface
FAN_PIN = 17
COOL_PIN = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(FAN_PIN, GPIO.IN)
GPIO.setup(COOL_PIN, GPIO.IN)

# Setup WeMo switches
WEMO_SERIAL_FAN = "os.environ['FAN_SERIAL_NUMBER']"
WEMO_SERIAL_COOL = "os.environ['COOL_SERIAL_NUMBER']"
WEMO_FAN = None
WEMO_COOL = None

# TODO: Make it specify based on IP rather than serial number
for device in pywemo.discover_devices():
  print "Found WeMo: " + device.serialnumber
  if device.serialnumber == WEMO_SERIAL_FAN:
    WEMO_FAN = device
  elif device.serialnumber == WEMO_SERIAL_COOL:
    WEMO_COOL = device


# Main Loop
while True:
  thermostat_cool_state = GPIO.input(COOL_PIN)
  wemo_cool_state = WEMO_COOL.get_state()

  print "**Cool*"
  print "Thermostat Cool is: " + str(wemo_cool_state)
  print "WeMo Cool is: " + str(thermostat_cool_state)
  if wemo_cool_state != thermostat_cool_state:
    if thermostat_cool_state:
      WEMO_COOL.on()
    else:
      WEMO_COOL.off()

  # We can run this without the fan attached, but no AC is fatal.
  print "**Fan**"
  thermostat_fan_state = GPIO.input(FAN_PIN)
  if WEMO_FAN:
    wemo_fan_state = WEMO_FAN.get_state()

    if wemo_fan_state != thermostat_fan_state:
      if thermostat_fan_state:
        WEMO_FAN.on()
      else:
        WEMO_FAN.off()
    print "Thermostat Fan is: " + str(thermostat_fan_state)
    print "WeMo Fan is: " + str(wemo_fan_state)
  else:
    print "Thermostat Fan is: " + str(thermostat_fan_state)
    print "WeMo Fan is not attached!"


  print "---"
  time.sleep(5)
