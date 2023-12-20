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

def paginate(data, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]


# customers endpoint to view content of customer table
@customers_bp.route("/customers", methods=["GET"])
def customers():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"
    

    # Fething all customers from database
    customers=db.select_all_customers()
    
    # Parsing page number parameter
    page = int(request.args.get('page', 1))
    # Number of items per page
    per_page = 10  

    # Paginate the data
    paginated_items = paginate(customers, page, per_page)

    
    return render_template('customers.html', customers=paginated_items, page=page)


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