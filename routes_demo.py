import paho.mqtt.client as mqtt
import threading
import time
import json
from datetime import datetime, timezone
from copy import deepcopy

broker_address = "16.58.46.198"
broker_port = 1883
client_id = "gps-simulator-teltonika"

# Create a MQTT client instance
client = mqtt.Client(client_id=client_id)

# Connect with retry (in case emqx is not ready yet)
while True:
    try:
        client.connect(broker_address, broker_port)
        print("✅ Connected to MQTT broker")
        break
    except Exception as e:
        print(f"⚠️ Connection failed: {e}. Retrying in 5 seconds...")
        time.sleep(5)

def get_current_timestamp():
    """Generate timestamp with milliseconds in ISO format"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+00:00"

def publish_to_topic(gps_data):
    """
    Publishes GPS location data for a single vehicle
    """
    locations = gps_data['position']['locations']
    num_locations = len(locations)
    index = 0
    
    while True:
        # Get current location
        current_location = locations[index]
        
        # Create a deep copy of the GPS data to avoid modifying the original
        payload = deepcopy(gps_data)
        
        # Remove the locations array from the payload
        del payload['position']['locations']
        
        # Add the current location data to position (converting to float)
        payload['position']['latitude'] = current_location['latitude']
        payload['position']['longitude'] = current_location['longitude']
        payload['position']['speed'] = float(current_location['speed'])
        payload['position']['course'] = float(current_location['course'])
        
        # Update timestamps
        current_time = get_current_timestamp()
        payload['position']['serverTime'] = current_time
        payload['position']['deviceTime'] = current_time
        payload['position']['fixTime'] = current_time
        payload['device']['lastUpdate'] = current_time
        
        # Convert to JSON
        json_message = json.dumps(payload)
        
        # Publish to topic using device uniqueId
        topic = f"location_vehicles/{gps_data['device']['uniqueId']}"
        client.publish(topic, json_message)
        print(f"Sent to {topic}: lat={current_location['latitude']}, lon={current_location['longitude']}, speed={float(current_location['speed'])}, course={float(current_location['course'])}")
        
        # Move to next location (loop back to start when finished)
        index = (index + 1) % num_locations
        
        # Wait 1 second before next update
        time.sleep(1.0)

# Load the JSON file with GPS data
with open('gps_simulation_data.json', 'r') as file:
    gps_devices = json.load(file)

# Create threads for each GPS device
VEHICLES_QUANTITY = 0
MAX_VEHICLES = 15
threads = []

for gps_data in gps_devices:
    if VEHICLES_QUANTITY >= MAX_VEHICLES:
        break
    
    thread = threading.Thread(target=publish_to_topic, args=(gps_data,))
    threads.append(thread)
    VEHICLES_QUANTITY += 1
    print(f"Starting simulation for device: {gps_data['device']['name']} (ID: {gps_data['device']['uniqueId']})")

# Start all threads
for thread in threads:
    thread.start()

print(f"\n🚀 Simulating {VEHICLES_QUANTITY} GPS devices...")
print("Press Ctrl+C to stop\n")