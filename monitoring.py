#
# Mqttagent that monitor a specific plateform (RAM, Disk, CPU , ... )
#

import paho.mqtt.client as mqtt
import time
import configparser
import os.path

import traceback

config = configparser.RawConfigParser()

import socket
hostname = socket.gethostname()

METRICS_MONITORING="home/agents/monitoring/plateform/" + hostname + "/metrics"


#############################################################
## MAIN

conffile = os.path.expanduser('~/.mqttagents.conf')
if not os.path.exists(conffile):
   raise Exception("config file " + conffile + " not found")

config.read(conffile)


username = config.get("agents","username")
password = config.get("agents","password")
mqttbroker = config.get("agents","mqttbroker")

client2 = mqtt.Client()

# client2 is used to send events to wifi connection in the house 
client2.username_pw_set(username, password)
client2.connect(mqttbroker, 1883, 60)

client = mqtt.Client();
client.username_pw_set(username, password)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("connected")

latesttime = None
cpt = 0

def on_message(client, userdata, msg):
   try:
      pass 
   except:
      traceback.print_exc();
 
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttbroker, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client2.loop_start()
client.loop_start()

lastvalue = None

import shutil
import psutil


# print("Total: %d GiB" % (total // (2**30)))
# print("Used: %d GiB" % (used // (2**30)))
# print("Free: %d GiB" % (free // (2**30)))

while True:
   try:
      time.sleep(3)
      total, used, free = shutil.disk_usage("/")
      client2.publish(METRICS_MONITORING + "/diskavailableG", str(free // (2**30)))
      client2.publish(METRICS_MONITORING + "/totaldiskG", str(total // (2**30)))
      client2.publish(METRICS_MONITORING + "/percentfree", str(int(free/total * 100)))


      client2.publish(METRICS_MONITORING + "/cpu", str(psutil.cpu_percent()))


   except Exception:
        traceback.print_exc()



