import psutil
import time
import requests
import json
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configurable variables
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:5000/update/device2")
SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", 10))  # Default to 10 seconds

def collect_system_stats():
    """Collects system statistics and sends them to the server."""
    data = {
        "cpu": psutil.cpu_percent(interval=None),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "bytes_sent": psutil.net_io_counters().bytes_sent,
        "bytes_recv": psutil.net_io_counters().bytes_recv,
        "uptime": time.time() - psutil.boot_time(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    headers = {"Connection": "close"}

    try:
        logging.info("Sending data to server...")
        response = requests.post(SERVER_URL, json=data, headers=headers, timeout=5)
        response.raise_for_status()
        logging.info("Data sent successfully!")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending data: {e}")

if __name__ == "__main__":
    try:
        while True:
            collect_system_stats()
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        logging.info("Stopping data collection.")
