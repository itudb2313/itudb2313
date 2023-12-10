from flask import render_template, request, redirect, url_for, jsonify
from app import app, db



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