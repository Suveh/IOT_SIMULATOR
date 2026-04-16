# IoT Device Simulator (MQTT - Mosquitto)

## Project Overview

This project simulates **500 virtual IoT devices** that connect to a local MQTT broker (Mosquitto) and continuously send sensor data in JSON format.
Each device behaves like a real IoT sensor, publishing temperature, humidity, and pressure data.


## Features

*  500 virtual IoT devices
*  MQTT communication using Mosquitto
*  Real-time data streaming
*  JSON formatted sensor data
*  Multi-threaded simulation


## Technologies Used

* Python
* MQTT (Mosquitto)
* paho-mqtt library


## Project Structure

simulator/
│── iot_simulator.py
│── README.md


##  Setup Instructions

### 1. Install Mosquitto

Download and install Mosquitto:
https://mosquitto.org/download/


### 2. Install Python Library

pip install paho-mqtt


### 3. Run Mosquitto Broker

(May already run as a service)

mosquitto


### 4. Run Simulator

python iot_simulator.py


### 5. Subscribe to Data

mosquitto_sub -h localhost -t "protonest/devices/#"


## 📡 Example Output

{
  "device_id": "protonesttest2001",
  "timestamp": "2026-04-16T10:25:30",
  "temperature": 28.5,
  "humidity": 65.2,
  "pressure": 1008.3
}


##  Device Naming Convention

Devices are named as:

protonesttest2001 → protonesttest2500


##  Future Improvements

* Async implementation for scalability (10,000+ devices)
* Cloud integration (AWS IoT / Firebase)
* Real-time dashboard (React / Next.js)
* Data storage (MongoDB / MySQL)


## Notes

This project demonstrates basic IoT communication using MQTT and device simulation techniques.
