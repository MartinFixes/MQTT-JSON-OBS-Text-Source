import json
import time
from obswebsocket import obsws, requests
import paho.mqtt.client as mqtt

# Configuration
MQTT_BROKER = "192.168.1.102"
MQTT_PORT = 1883
MQTT_TOPIC = "path/to/topic"
OBS_HOST = "192.168.1.101"
OBS_PORT = 4455
OBS_PASSWORD = "password"

# Connect to OBS
def connect_to_obs():
    ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
    try:
        ws.connect()
        print("Connected to OBS WebSocket")
    except Exception as e:
        print(f"Failed to connect to OBS: {e}")
        ws = None
    return ws

# Update OBS Text Source
def update_obs_text_source(ws, source_name, text):
    try:
        ws.call(requests.SetInputSettings(inputName=source_name, inputSettings={"text": text,}))
        print(f"Updated OBS source '{source_name}' with text: {text}")
    except Exception as e:
        print(f"Failed to update OBS source '{source_name}': {e}")


# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect to MQTT broker: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received MQTT message: {payload}")
    try:
        data = json.loads(payload)
        if isinstance(data, dict):
            for key, value in data.items():
                update_obs_text_source(userdata['obs_ws'], key, str(value))
        else:
            print("Invalid JSON payload: Expected a dictionary")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")

# Main Function
def main():
    # Connect to OBS
    obs_ws = connect_to_obs()
    if not obs_ws:
        return

    # Set up MQTT client
    client = mqtt.Client(userdata={"obs_ws": obs_ws})
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return

    # Start MQTT loop
    try:
        client.loop_start()
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        print("Stopping script...")
    finally:
        client.loop_stop()
        client.disconnect()
        obs_ws.disconnect()
        print("Disconnected from MQTT and OBS")

if __name__ == "__main__":
    main()
