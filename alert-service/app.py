from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

INVENTORY_SERVICE_URL = "http://127.0.0.1:5001"

@app.route('/')
def home():
    return "Alert Service Running!"

# GET LOW STOCK ITEMS
@app.route('/alerts/low-stock', methods=['GET'])
def low_stock_alerts():
    try:
        response = requests.get(f"{INVENTORY_SERVICE_URL}/inventory")
        inventory = response.json()

        low_stock_items = [
            item for item in inventory if item["quantity"] < item["threshold"]
        ]

        return jsonify({
            "low_stock_count": len(low_stock_items),
            "items": low_stock_items
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5002, debug=True)