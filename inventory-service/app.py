from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ==============================
# Database Configuration
# ==============================
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'SHA$#@nk25)42))3'
app.config['MYSQL_DB'] = 'inventory_system'
mysql = MySQL(app)


# ==============================
# Helper Functions
# ==============================
def get_cursor():
    return mysql.connection.cursor()


def validate_inventory_data(data, update=False):
    required_fields = ['name', 'category', 'quantity', 'threshold', 'unit']

    if not data:
        return "No input data provided"

    for field in required_fields:
        if field not in data:
            return f"{field} is required"

    if not isinstance(data['quantity'], (int, float)) or data['quantity'] < 0:
        return "Quantity must be a positive number"

    if not isinstance(data['threshold'], (int, float)) or data['threshold'] < 0:
        return "Threshold must be a positive number"

    if data['category'] not in ['RAW', 'FINISHED']:
        return "Category must be either 'RAW' or 'FINISHED'"

    return None


# ==============================
# Routes
# ==============================

@app.route('/')
def home():
    return jsonify({"message": "Inventory Backend Running!"})


# GET ALL INVENTORY
@app.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        cur = get_cursor()
        cur.execute("SELECT * FROM inventory")
        rows = cur.fetchall()
        cur.close()

        inventory_list = [
            {
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "quantity": row[3],
                "threshold": row[4],
                "unit": row[5],
                "created_at": row[6],
                "lowStock": row[3] < row[4]
            }
            for row in rows
        ]

        return jsonify(inventory_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ADD NEW INVENTORY ITEM
@app.route('/inventory', methods=['POST'])
def add_inventory():
    try:
        data = request.get_json()
        error = validate_inventory_data(data)

        if error:
            return jsonify({"error": error}), 400

        cur = get_cursor()
        cur.execute("""
            INSERT INTO inventory (name, category, quantity, threshold, unit)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['name'],
            data['category'],
            data['quantity'],
            data['threshold'],
            data['unit']
        ))

        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Item added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# UPDATE INVENTORY ITEM
@app.route('/inventory/<int:item_id>', methods=['PUT'])
def update_inventory(item_id):
    try:
        data = request.get_json()
        error = validate_inventory_data(data)

        if error:
            return jsonify({"error": error}), 400

        cur = get_cursor()
        cur.execute("SELECT id FROM inventory WHERE id = %s", (item_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"error": "Item not found"}), 404

        cur.execute("""
            UPDATE inventory
            SET name=%s, category=%s, quantity=%s, threshold=%s, unit=%s
            WHERE id=%s
        """, (
            data['name'],
            data['category'],
            data['quantity'],
            data['threshold'],
            data['unit'],
            item_id
        ))

        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Item updated successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE INVENTORY ITEM
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory(item_id):
    try:
        cur = get_cursor()
        cur.execute("SELECT id FROM inventory WHERE id = %s", (item_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"error": "Item not found"}), 404

        cur.execute("DELETE FROM inventory WHERE id = %s", (item_id,))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Item deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# INVENTORY SUMMARY
@app.route('/inventory/summary', methods=['GET'])
def inventory_summary():
    try:
        cur = get_cursor()

        cur.execute("SELECT COUNT(*) FROM inventory")
        total_items = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM inventory WHERE category = 'RAW'")
        total_raw = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM inventory WHERE category = 'FINISHED'")
        total_finished = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM inventory WHERE quantity < threshold")
        low_stock = cur.fetchone()[0]

        cur.close()

        return jsonify({
            "total_items": total_items,
            "total_raw": total_raw,
            "total_finished": total_finished,
            "low_stock_items": low_stock
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==============================
# App Runner
# ==============================
if __name__ == '__main__':
    app.run(port=5001, debug=True)
