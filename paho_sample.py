import paho.mqtt.client as mqtt
import pywemo
import os

# WeMo initial setup
WEMO_SERIAL_FAN = os.environ['FAN_SERIAL_NUMBER']
WEMO_SERIAL_COOL = os.environ['COOL_SERIAL_NUMBER']
WEMO_FAN = None
WEMO_COOL = None

# TODO: Make it specify based on IP rather than serial number
for device in pywemo.discover_devices():
    print "Found WeMo: " + device.serialnumber
    if device.serialnumber == WEMO_SERIAL_FAN:
      WEMO_FAN = device
    elif device.serialnumber == WEMO_SERIAL_COOL:
      WEMO_COOL = device


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("air_conditioner/set")
    client.subscribe("fan/set")
    client.subscribe("ignore_thermostat/set")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if '/set' in msg.topic:
      topic_to_update = msg.topic[:-3] + 'status'

      print('setting ' + topic_to_update + ' to ' + msg.payload)

      # do stuff
      # TODO: Make more generic
      device=None

      if 'air_conditioner' in msg.topic:
        device = WEMO_COOL
      elif 'fan' in msg.topic:
        device = WEMO_FAN

      if int(msg.payload):
        device.on()
      else:
        device.off()

      client.publish(topic_to_update,payload=msg.payload,retain=True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.200")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
while True:
    client.loop()
