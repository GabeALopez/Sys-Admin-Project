from flask import Flask, request, jsonify, render_template
import psutil
import time

app = Flask(__name__)

# Dictionary to store latest data from each device
devices_data = {
    "device1": {},
    "device2": {},
    "device3": {}
}

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

@app.route("/")
def index():
    return render_template("index.html")  # Load the dashboard

@app.route("/update/<device_id>", methods=["POST"])
def update_device(device_id):
    """Receive system data from agents"""
    if device_id in devices_data:
        devices_data[device_id] = request.json
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid device"}), 400

@app.route("/data", methods=["GET"])
def get_data():
    """Return latest data for all devices"""
    return jsonify(devices_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
