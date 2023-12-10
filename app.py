from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database


app = Flask(__name__)
app.config.from_object("config")
with app.app_context():
    db = Database()
    

import endpoints.orders
import endpoints.customers
import endpoints.employees
import endpoints.rises



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

@app.route("/stores",methods=["GET"])
def stores():
    return render_template("stores.html", stores=db.get_all_stores_table(), headers=db.get_stores_columns() , stores_count = db.get_stores_count())

@app.route("/stores_table",methods=["GET"])
def stores_table():
    order_opt = request.args.get("order_opt")
    page_number = request.args.get("page_number")
    print("hereeeeeeeeeeeeeEEEEEEEEEEEEEEEEe123123ee " + page_number)
    stores = db.get_all_stores_table(order_opt=order_opt, page_number=page_number)
    return render_template("stores_table.html", stores=stores, headers=db.get_stores_columns() )


@app.route("/products")
def get_products():
    searchword = request.args.get("search", "")
    searchword = "%" + searchword + "%"
    return render_template("products.html", products=db.get_products(search=searchword))


@app.route("/insert_product", methods=["GET"])
def get_insert_product_page():
    return render_template(
        "insert_product.html",
        providers=db.get_providers(),
        categories=db.select_all_categories(),
    )


@app.route("/delete_product", methods=["POST"])
def delete_product():
    product_id = request.json.get("product_id")
    db.delete_product(product_id)
    return redirect(url_for("get_products"))
    

@app.route("/insert_product", methods=["POST"])
def insert_product():
    product_name = request.form["name"]
    model = request.form["model"]
    year = request.form["year"]
    color = request.form["color"]
    price = request.form["price"]
    km = request.form["mileage"]
    category_id = request.form["category_id"]
    provider_id = request.form["provider_id"]
    if db.insert_product(product_name ,model, year, color, price, km, category_id, provider_id):
        return redirect(url_for("get_products"))
    else:
        return ["Error"]


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
