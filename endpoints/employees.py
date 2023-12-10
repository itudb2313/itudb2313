from flask import render_template, request, redirect, url_for, jsonify
from app import app, db



# customers endpoint to view content of customer table
@app.route("/employees", methods=["GET"])
def employees():
    return render_template("employees.html", employees=db.select_all_employees())


# insert_employee endpoint to insert new employee record into the employee table
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


# delete_employee endpoint to delete an employee record by employee_id
@app.route("/delete_employee", methods=["POST"])
def delete_employee():
    if request.method == "POST":
        employee_id = request.form["employee_id"]

        db.delete_employee(employee_id)

        return redirect(url_for("employees"))