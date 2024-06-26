from flask import (
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    current_app,
    Blueprint,
)

employees_bp = Blueprint("employees_bp", __name__)

def paginate(data, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]

# employees endpoint to view content of customer table
@employees_bp.route("/employees", methods=["GET"])
def employees():

    db = current_app.config.get("db")

    if db is None:
        return "No database found"
    
    # Fething all employees from database
    employees=db.select_all_employees()
    topEmployees=db.select_top_ten_employees()
    mostPayed = db.select_most_paid_employees()
    
    # Parsing page number parameter
    page = int(request.args.get('page', 1))
    # Number of items per page
    per_page = 30  

    # Paginate the data
    paginated_items = paginate(employees, page, per_page)

    return render_template("employees.html", employees=paginated_items, topEmployees=topEmployees, mostPayed=mostPayed, page=page)


@employees_bp.route("/get_employee_by_id", methods=["GET"])
def get_employee_by_id():

    db = current_app.config.get("db")

    if db is None:
        return "No database found"
    
    employee_id = request.args.get('employee_id')
    
    employee = db.get_employee_by_id(employee_id)

    return jsonify({"employee": employee})


# insert_employee endpoint to insert new employee record into the employee table
@employees_bp.route("/insert_employee", methods=["GET", "POST"])
def insert_employee():

    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        employee_id = request.form["employee_id"]
        store_id = request.form["store_id"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        dob = request.form["dob"]
        email = request.form["email"]
        status = request.form["status"]
        salary = request.form["salary"]
        city = request.form["city"]
        country = request.form["country"]

        db.insert_employee(
            employee_id,
            store_id,
            firstname,
            lastname,
            dob,
            email,
            status,
            salary,
            city,
            country,
        )
        #return render_template("employees.html", employees=db.select_all_employees())
        return redirect(url_for('employees_bp.employees'))
    else:
        return render_template("insert_employee.html")
    

@employees_bp.route("/update_employee", methods=["GET", "POST"])
def update_employee():

    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        employee_id = request.form["employee_id"]
        store_id = request.form["store_id"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        dob = request.form["dob"]
        email = request.form["email"]
        status = request.form["status"]
        salary = request.form["salary"]
        city = request.form["city"]
        country = request.form["country"]

        db.update_employee_by_id(
            employee_id,
            store_id,
            firstname,
            lastname,
            dob,
            email,
            status,
            salary,
            city,
            country,
        )
        #return render_template("employees.html", employees=db.select_all_employees())
        return redirect(url_for('employees_bp.employees'))
    else:
        return render_template("update_employee.html")


# delete_employee endpoint to delete an employee record by employee_id
@employees_bp.route("/delete_employee", methods=["GET","POST"])
def delete_employee():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        employee_id = request.form["employee_id"]

        db.delete_employee_by_id(employee_id)

        return redirect(url_for("employees_bp.employees"))
    else:
        if request.args.get('employee_id') is not None:
            employee_id = int(request.args.get('employee_id'))
            db.delete_employee_by_id(employee_id)

        return redirect(url_for("employees_bp.employees"))