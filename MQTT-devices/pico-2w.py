import board, time, digitalio # board dependency
import json
import random
import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT

# Setup LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Function to control number of flashes and flash interval 
def flash_led(times=10, interval=1):
    """Flash the external LED rapidly a specified number of times."""
    for _ in range(times):
        led.value = True  # Turn on the LED
        time.sleep(interval)
        led.value = False  # Turn off the LED
        time.sleep(interval)

print("Blinking LED ...")
# Flash the external LED 5 times rapidly
flash_led(2, 0.5)



# Load Wi-Fi and MQTT credentials
try:
    from secrets import secrets
except ImportError:
    print("Wi-Fi and MQTT secrets are missing in secrets.py!")
    raise

# Connect to Wi-Fi
print("Connecting to Wi-Fi...")
wifi.radio.connect(secrets["ssid"], secrets["password"])
print(f"Connected to Wi-Fi! IP Address: {wifi.radio.ipv4_address}")

# Create a socket pool for MQTT
pool = socketpool.SocketPool(wifi.radio)

# Define MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker!")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker!")

def on_publish(client, userdata, topic, pid):
    print(f"Message published to {topic}.")

# Set up MQTT client
mqtt_client = MQTT.MQTT(
    broker=secrets["mqtt_broker"],
    port=secrets["mqtt_port"],
    username=secrets["mqtt_username"],
    password=secrets["mqtt_password"],
    socket_pool=pool
)

topic=secrets["mqtt_topic"]
sensor_id=secrets["sensor_id"]
 

# Assign callback functions
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_publish = on_publish

# Connect to MQTT broker
# print("Connecting to MQTT broker...")
print(f"Connecting to MQTT broker {secrets["mqtt_broker"]} ...")
mqtt_client.connect()

# Main loop
try:
    while True:
        # Generate a random value
        random_value = random.uniform(0, 100)  # Random float between 0 and 100

        # Create a JSON-encoded message
        # { "SensorID": "ABC123",  "temperature": 22.54 }
        
        message = json.dumps({"SensorID": sensor_id, "temperature": random_value})

        # Publish the message to a topic
        # topic = "pico/random_value"
        
        print(f"Publishing to {topic}: {message}")
        mqtt_client.publish(topic, message)
        flash_led(2, 0.2)

        # Wait before sending the next message
        time.sleep(9)

except KeyboardInterrupt:
    print("Disconnecting from MQTT broker...")
    mqtt_client.disconnect()
    print("Program stopped.")