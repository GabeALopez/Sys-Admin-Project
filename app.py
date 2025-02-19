from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

latest_data = {"cpu": 0, "memory": 0, "disk": 0}

@app.route("/")
def index():
    return render_template("index.html")  # Serves the dashboard

@app.route("/update", methods=["POST"])
def update_data():
    global latest_data
    latest_data = request.json
    return jsonify({"status": "success"}), 200

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(latest_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

