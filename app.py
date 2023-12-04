from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database

app = Flask(__name__)
app.config.from_object("config")
with app.app_context():
    db = Database()

import endpoints.orders


@app.route("/")
def hello_world():
    return render_template("index.html")


# categories endpoint to view content of categories table
@app.route("/categories", methods=["GET"])
def categories():
    return render_template("categories.html", categories=db.select_all_categories())


# customers endpoint to view content of customer table
@app.route("/customers", methods=["GET"])
def customers():
    return render_template("customers.html", customers=db.select_all_customers())


# insert_customer endpoint to insert new customer record into the customer table
@app.route("/insert_customer", methods=["GET", "POST"])
def insert_customer():
    if request.method == "POST":
        customer_id = request.form["customer_id"]
        employee_id = request.form["employee_id"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        dof = request.form["dof"]
        phone = request.form["phone"]
        email = request.form["email"]
        city = request.form["city"]
        country = request.form["country"]

        print(
            customer_id,
            employee_id,
            firstname,
            lastname,
            dof,
            phone,
            email,
            city,
            country,
        )

        db.insert_customer(
            customer_id,
            employee_id,
            firstname,
            lastname,
            dof,
            phone,
            email,
            city,
            country,
        )
        return render_template("customers.html", customers=db.select_all_customers())
    else:
        return render_template("insert_customer.html")


# customers endpoint to view content of customer table
@app.route("/employees", methods=["GET"])
def employees():
    return render_template("employees.html", employees=db.select_all_employees())


@app.route("/stores")
def stores():
    return render_template(
        "stores.html", stores=db.get_all_stores(), headers=db.get_stores_columns()
    )


# insert_customer endpoint to insert new customer record into the customer table
@app.route("/insert_employee", methods=["GET", "POST"])
def insert_employee():
    if request.method == "POST":
        employee_id = request.form["employee_id"]
        store_id = request.form["store_id"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        dof = request.form["dof"]
        phone = request.form["phone"]
        email = request.form["email"]
        status = request.form["status"]
        salary = request.form["salary"]
        street = request.form["street"]
        city = request.form["city"]
        country = request.form["country"]

        db.insert_employee(
            employee_id,
            store_id,
            firstname,
            lastname,
            dof,
            phone,
            email,
            status,
            salary,
            street,
            city,
            country,
        )
        return render_template("employees.html", employees=db.select_all_employees())
    else:
        return render_template("insert_employee.html")


# insert_customer endpoint to insert new customer record into the customer table
@app.route("/delete_customer", methods=["GET", "POST"])
def delete_customer():
    if request.method == "POST":
        customer_id = request.form["customer_id"]

        db.delete_customer(customer_id)

        return render_template("customers.html", customers=db.select_all_customers())


# rises endpoint to view content of rise_archive table
@app.route("/rises", methods=["GET"])
def rises():
    return render_template("rises.html", rises=db.select_all_rises())


# insert_rise endpoint to insert new rise record into the rise_archive table
@app.route("/insert_rise", methods=["GET", "POST"])
def insert_rise():
    if request.method == "POST":
        rise_id = request.form["rise_id"]
        amount_by_percent = request.form["amount_by_percent"]
        rise_date = request.form["rise_date"]
        rise_state = request.form["rise_state"]

        db.insert_rise(rise_id, amount_by_percent, rise_date, rise_state)
        return redirect(url_for("rises"))
    else:
        return render_template("insert_rise.html", rises=db.select_all_rises())


@app.route("/products")
def get_products():
    searchword = request.args.get("search", "")
    searchword = "%" + searchword + "%"
    return jsonify(db.get_products(search=searchword))


@app.route("/providers")
def get_providers():
    searchword = request.args.get("search", "")
    searchword = "%" + searchword + "%"
    start_debt = request.args.get("from", "")
    end_debt = request.args.get("to", "")
    return jsonify(db.get_providers(search=searchword, start=start_debt, to=end_debt))


@app.route("/providers/countries")
def get_proiveder_countries():
    return jsonify(db.get_provider_countries())


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
