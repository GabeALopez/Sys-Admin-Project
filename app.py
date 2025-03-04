from flask import Flask, request, jsonify, render_template
import psutil
import time
import os

app = Flask(__name__)

# Dictionary to store latest data from each device
devices_data = {
    "device1": {},
    "device2": {},
    "device3": {}
}

# Paths
fifo_name = "/tmp/my_named_pipe"
log_file_path = "/tmp/device_data.log"

# Create the named pipe if it does not exist
if not os.path.exists(fifo_name):
    os.mkfifo(fifo_name)

def get_system_info():
    """Collect system usage info"""
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "bytes_sent": psutil.net_io_counters().bytes_sent,
        "bytes_recv": psutil.net_io_counters().bytes_recv,
        "uptime": time.time() - psutil.boot_time()
    }

def write_to_storage(data):
    """Write data to both the log file and the FIFO"""
    
    # Write to log file (for history)
    with open(log_file_path, "a") as log_file:
        log_file.write(data + '\n')
    
    # Write to FIFO (for real-time updates)
    try:
        with open(fifo_name, 'w') as fifo:
            fifo.write(data + '\n')
    except BrokenPipeError:
        print("No process is reading from the FIFO.")

def read_from_fifo():
    """Read from FIFO, if available"""
    try:
        with open(fifo_name, 'r') as fifo:
            return fifo.read().strip()
    except FileNotFoundError:
        return "FIFO not available"

def read_log():
    """Read the last 10 entries from the log file"""
    try:
        with open(log_file_path, "r") as log_file:
            return log_file.readlines()[-10:]  # Return last 10 entries
    except FileNotFoundError:
        return []

@app.route("/")
def index():
    return render_template("index.html")  # Load the dashboard

@app.route("/update/<device_id>", methods=["POST"])
def update_device(device_id):
    """Receive system data from agents and write to both FIFO and log"""
    if device_id in devices_data:
        devices_data[device_id] = request.json
        data_to_write = f"{device_id}: {request.json}"
        write_to_storage(data_to_write)  # Store in both FIFO and log
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid device"}), 400

@app.route("/data", methods=["GET"])
def get_data():
    """Return both latest FIFO data and historical log data"""
    latest_fifo = read_from_fifo()
    historical_logs = read_log()
    
    return jsonify({
        "latest_fifo": latest_fifo,
        "history": historical_logs,
        "devices_data": devices_data
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

