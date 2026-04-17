import json
import time
import random
import threading
import ssl
import os
from datetime import datetime, UTC

import paho.mqtt.client as mqtt

BROKER = "mqtt.protonest.co"
PORT = 8883
TOPIC_BASE = "protonest/devices"

NUM_DEVICES = 10   # start with 10
START_ID = 1

PASSWORD = os.getenv("MQTT_PASSWORD")


def generate_sensor_data(device_id):
    return {
        "device_id": device_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "pressure": round(random.uniform(950, 1050), 2)
    }


def run_device(num):
    username = f"test-protonest#num#{num}"
    client_id = username

    client = mqtt.Client(client_id=client_id)

    # Authentication
    client.username_pw_set(username=username, password=PASSWORD)

    # TLS (required for mqtts)
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)

    try:
        client.connect(BROKER, PORT, 60)
        client.loop_start()
        print(f"[CONNECTED] {client_id}")
    except Exception as e:
        print(f"[ERROR] {client_id} connection failed:", e)
        return

    safe_client_id = client_id.replace("#", "_")
    topic = f"{TOPIC_BASE}/{safe_client_id}"

    while True:
        data = generate_sensor_data(client_id)
        payload = json.dumps(data)

        client.publish(topic, payload)
        print(f"[{client_id}] Sent")

        time.sleep(random.uniform(1, 3))


def main():
    threads = []

    for i in range(START_ID, START_ID + NUM_DEVICES):
        t = threading.Thread(target=run_device, args=(i,))
        t.daemon = True
        t.start()

        threads.append(t)
        time.sleep(0.2)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()