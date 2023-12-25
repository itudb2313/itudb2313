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
    oldcustomers=db.oldest_customers_with_employee()
    
    # Parsing page number parameter
    page = int(request.args.get('page', 1))
    # Number of items per page
    per_page = 30  

    # Paginate the data
    paginated_items = paginate(customers, page, per_page)

    
    return render_template('customers.html', customers=paginated_items, oldcustomers=oldcustomers, page=page)


@customers_bp.route("/get_customer_by_id", methods=["GET"])
def get_customer_by_id():

    db = current_app.config.get("db")

    if db is None:
        return "No database found"
    
    customer_id = request.args.get('customer_id')
    
    customer = db.get_customer_by_id(customer_id)

    return jsonify({"customer": customer})


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
        
        return redirect(url_for('customers_bp.customers'))
    else:
        return render_template("insert_customer.html")
    

@customers_bp.route("/update_customer", methods=["GET", "POST"])
def update_customer():

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

        db.update_customer_by_id(
            customer_id,
            employee_id,
            firstname,
            lastname,
            dob,
            email,
            city,
            country,
        )
        return redirect(url_for('customers_bp.customers'))
    else:
        return render_template("update_customer.html")
    


@customers_bp.route("/delete_customer", methods=["GET","POST"])
def delete_customer():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        customer_id = request.form["customer_id"]

        db.delete_customer_by_id(customer_id)

        return redirect(url_for("customers_bp.customers"))
    
    else:
        if request.args.get('customer_id') is not None:
            customer_id = int(request.args.get('customer_id'))
            db.delete_customer_by_id(customer_id)

        return redirect(url_for("customers_bp.customers"))