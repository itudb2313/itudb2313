from flask import (
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    current_app,
    Blueprint,
)

customers_bp = Blueprint("customers_bp", __name__)


# customers endpoint to view content of customer table
@customers_bp.route("/customers", methods=["GET"])
def customers():

    db = current_app.config.get("db")

    if db is None:
        return "No database found"
    
    return render_template("customers.html", customers=db.select_all_customers())


# insert_customer endpoint to insert new customer record into the customer table
@customers_bp.route("/insert_customer", methods=["GET", "POST"])
def insert_customer():

    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        customer_id = request.form["customer_id"]
        employee_id = request.form["employee_id"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        dob = request.form["dob"]
        email = request.form["email"]
        city = request.form["city"]
        country = request.form["country"]

        db.insert_customer(
            customer_id,
            employee_id,
            firstname,
            lastname,
            dob,
            email,
            city,
            country,
        )
        return render_template("customers.html", customers=db.select_all_customers())
    else:
        return render_template("insert_customer.html")