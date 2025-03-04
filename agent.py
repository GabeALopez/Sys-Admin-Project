import psutil
import time
import requests
import json
from datetime import datetime

# Change this for each device (device1, device2, device3, etc.)
SERVER_URL = "http://localhost:5000/update/device1"

def collect_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    disk = psutil.disk_usage('/')
    disk_usage = disk.percent

    net = psutil.net_io_counters()
    bytes_sent = net.bytes_sent
    bytes_recv = net.bytes_recv

    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp to the second

    # Create the data payload to match what the server expects
    data = {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "disk": disk_usage,
        "bytes_sent": bytes_sent,
        "bytes_recv": bytes_recv,
        "uptime": uptime,
        "timestamp": timestamp  # Add the timestamp to the data
    }

    try:
        response = requests.post(SERVER_URL, json=data)
        if response.status_code == 200:
            print("Data sent successfully!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

while True:
    collect_system_stats()
    time.sleep(10)
