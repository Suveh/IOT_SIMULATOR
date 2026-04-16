import json
import time
import random
import threading
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC_BASE = "protonest/devices"

NUM_DEVICES = 500
START_ID = 2001


def generate_sensor_data(device_id):
    return {
        "device_id": device_id,
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "pressure": round(random.uniform(950, 1050), 2)
    }


def run_device(device_id):
    client = mqtt.Client(client_id=device_id)

    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        print(f"[ERROR] {device_id} connection failed:", e)
        return

    topic = f"{TOPIC_BASE}/{device_id}"

    while True:
        data = generate_sensor_data(device_id)
        payload = json.dumps(data)

        client.publish(topic, payload)
        print(f"[{device_id}] Sent: {payload}")

        time.sleep(random.uniform(1, 3))  # simulate real device delay


def main():
    threads = []

    for i in range(NUM_DEVICES):
        device_id = f"protonesttest{START_ID + i}"

        t = threading.Thread(target=run_device, args=(device_id,))
        t.daemon = True
        t.start()

        threads.append(t)
        time.sleep(0.01)  # slight delay to avoid overload

    # Keep main thread alive
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()