from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

INVENTORY_SERVICE = "http://127.0.0.1:5001"
ALERT_SERVICE = "http://127.0.0.1:5002"

@app.route('/')
def home():
    return "API Gateway Running!"

# INVENTORY ROUTES
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'GET':
        response = requests.get(f"{INVENTORY_SERVICE}/inventory")
        return jsonify(response.json())
    
    if request.method == 'POST':
        response = requests.post(
            f"{INVENTORY_SERVICE}/inventory",
            json=request.get_json()
        )
        return jsonify(response.json()), response.status_code


@app.route('/inventory/<int:id>', methods=['PUT', 'DELETE'])
def inventory_by_id(id):
    if request.method == 'PUT':
        response = requests.put(
            f"{INVENTORY_SERVICE}/inventory/{id}",
            json=request.get_json()
        )
        return jsonify(response.json()), response.status_code
    
    if request.method == 'DELETE':
        response = requests.delete(
            f"{INVENTORY_SERVICE}/inventory/{id}"
        )
        return jsonify(response.json()), response.status_code


@app.route('/inventory/summary', methods=['GET'])
def summary():
    response = requests.get(f"{INVENTORY_SERVICE}/inventory/summary")
    return jsonify(response.json())


# ALERT ROUTES
@app.route('/alerts/low-stock', methods=['GET'])
def low_stock():
    response = requests.get(f"{ALERT_SERVICE}/alerts/low-stock")
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(port=5000, debug=True)