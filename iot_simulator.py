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

NUM_DEVICES = 500   # change to 200, 300 later
START_ID = 1

PASSWORD = os.getenv("MQTT_PASSWORD")

clients = []


def generate_sensor_data(device_id):
    return {
        "device_id": device_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "pressure": round(random.uniform(950, 1050), 2)
    }


def create_client(num):
    username = f"test-protonest#num#{num}"
    client_id = username

    client = mqtt.Client(client_id=client_id)

    client.username_pw_set(username=username, password=PASSWORD)

    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)

    return client, client_id


def connect_all():
    print("\nConnecting all devices...")

    for i in range(START_ID, START_ID + NUM_DEVICES):
        client, client_id = create_client(i)
        try:
            client.connect(BROKER, PORT, 60)
            client.loop_start()
            clients.append((client, client_id))

            time.sleep(0.05)  

        except Exception as e:
            print(f"[ERROR] {client_id}: {e}")
    print("All devices connected")


def send_all():
    print("\nSending data from all devices...")
    for client, client_id in clients:
        safe_client_id = client_id.replace("#", "_")
        topic = f"{TOPIC_BASE}/{safe_client_id}"

        data = generate_sensor_data(client_id)
        payload = json.dumps(data)

        client.publish(topic, payload)

    print("All devices sent data")


def disconnect_all():
    print("\nDisconnecting all devices...")
    for client, _ in clients:
        client.loop_stop()
        client.disconnect()

    print("All devices disconnected")


def run_test_cycle():
    connect_all()
    time.sleep(3)

    send_all()
    time.sleep(3)

    disconnect_all()


def main():
    print("Starting MQTT Load Test...\n")

    # Run multiple cycles
    for cycle in range(3):
        print(f"\nCycle {cycle + 1}")
        run_test_cycle()
        time.sleep(5)

    print("\nTest Completed")


if __name__ == "__main__":
    main()