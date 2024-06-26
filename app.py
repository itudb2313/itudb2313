from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
app.config.from_object("config")
with app.app_context():
    db = Database()
    app.config["db"] = db

from endpoints.categories import categories_bp
from endpoints.orders import orders_bp
from endpoints.customers import customers_bp
from endpoints.employees import employees_bp
from endpoints.rises import rises_bp
from endpoints.stores import stores_bp
from endpoints.products import products_bp
from endpoints.providers import providers_bp

app.register_blueprint(categories_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(rises_bp)
app.register_blueprint(stores_bp)
app.register_blueprint(products_bp)
app.register_blueprint(providers_bp)

@app.route("/")
def hello_world():
    return render_template("index.html")




# Example code snippet for json data transfer. Do not remove.
@app.route("/process_json", methods=["POST"])
def process_json():
    try:
        # Get the JSON data from the request
        json_data = request.get_json()

        # Access individual fields from the JSON data
        rise_id = json_data["rise_id"]
        amount_by_percent = json_data["amount_by_percent"]
        rise_date = json_data["rise_date"]
        rise_state = json_data["rise_state"]

        db.insert_rise(rise_id, amount_by_percent, rise_date, rise_state)

        # Return a response (you can customize this based on your needs)
        return jsonify({"message": "JSON data processed successfully"})

    except Exception as e:
        # Handle any exceptions or validation errors
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run()
