from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database

app = Flask(__name__)
app.config.from_object("config")
with app.app_context():
    db = Database()


@app.route("/")
def hello_world():
    return render_template("index.html")


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
def products():
    return render_template("products.html", products=db.get_all_products())


@app.route("/orders")
def orders():
    return render_template("orders.html", orders=db.get_orders_paged(10, 0))


@app.route("/get-orders", methods=["GET"])
def get_orders():
    page = int(request.args.get("page", 1))
    order_by = request.args.get("order_by", "order_id")
    t_order = request.args.get("order", "ASC")

    rows = """"""
    for order in db.get_orders_paged(10, page * 10, order_by, t_order):
        rows += f"""
            <tr>
            <td class="border">{order[0]}</td>
            <td class="border underline">
                <a href="/customer?id={order[1]}">{order[1]}</a>
            </td>
            <td class="border underline">
                <a href="/products?id={order[2]}">{order[2]}</a>
            </td>
            <td class="border underline">
                <a href="/stores?id={order[3]}">{order[3]}</a>
            </td>
            <td class="border underline">
                <a href="/employees?id={order[4]}">{order[4]}</a>
            </td>
            <td class="border">{order[5]}</td>
            <td class="border">{order[6]}</td>
            <td class="border">{order[7]}</td>
            <td class="border">{order[8]}</td>
            <td class="border">{order[9]}</td>
        </tr>"""

    return (
        rows
        + f"""
        <tr>
            <td colspan="10"
                hx-get="/get-orders?page={page+1}&order_by={order_by}&order={t_order}"
                hx-target="#replace"
                hx-swap="innerHTML">
                click for next page: {page+1}
            </td>
        </tr>
        """
    )


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


app.run()

