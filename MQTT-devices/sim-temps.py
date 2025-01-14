import time
import random
import paho.mqtt.client as mqtt
import json
from datetime import datetime, timezone, timedelta

# Current time in UTC
utc_time = datetime.now(timezone.utc)
print(utc_time.isoformat())  # e.g., "2025-01-06T14:23:45.678910+00:00"

# MQTT Broker details
BROKER = "127.0.0.1"  # Replace with your MQTT broker address
PORT = 1883                 # Default MQTT port
TOPIC = "sensor/temperature"  # Topic to publish to

# MQTT Client Setup
client = mqtt.Client()
client.connect(BROKER, PORT, 60)
iter = 1

# Simulate and send MQTT messages
try:
    while True : # iter <= 20:
        # Current Unix timestamp
        timestamp = int(time.time())
        
        # Simulated temperature
        temperature = round(random.uniform(5.0, 35.0), 2)  # Generate temperature between 15.0 and 30.0
        # iso = datetime.now().isoformat()
        
        # Current time in UTC
        utc_time = datetime.now(timezone.utc)
        # print(utc_time.isoformat())  # e.g., "2025-01-06T14:23:45.678910+00:00"
        iso = utc_time.isoformat()

        # Message payload
        payload = {
            "SensorID" : "PySimv1",
            "unixtime": timestamp,
            "isotime": iso,
            "temperature": temperature
        }
        


        # Publish the message
        client.publish(TOPIC,  json.dumps(payload))
        print(f"Published: { json.dumps(payload)}")
        
        # Sleep for 1 seconds (adjust as needed)
        time.sleep(5)
        iter += 1
        
except KeyboardInterrupt:
    print("Simulation stopped.")

# Disconnect the client
client.disconnect()