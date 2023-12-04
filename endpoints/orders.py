from flask import render_template, request, redirect, url_for, jsonify
from __main__ import app, db


table_columns = [
    {"name": "Order ID", "order_by": "order_id", "sortable": True},
    {"name": "Customer ID", "order_by": "customer_id", "sortable": False},
    {"name": "Product ID", "order_by": "product_id", "sortable": False},
    {"name": "Store ID", "order_by": "store_id", "sortable": False},
    {"name": "Employee ID", "order_by": "employee_id", "sortable": False},
    {"name": "Order Date", "order_by": "order_date", "sortable": True},
    {"name": "Ship Date", "order_by": "ship_date", "sortable": True},
    {"name": "Required Date", "order_by": "required_date", "sortable": True},
    {"name": "Order Status", "order_by": "order_status", "sortable": True},
    {"name": "Quantity", "order_by": "quantity", "sortable": True},
]


@app.route("/orders")
def orders():
    return render_template("orders.html", orders=db.get_orders_paged(10, 0))


def create_th(column, t_order):
    if column["sortable"]:
        return f"""
                <th class="border w-28" 
                    hx-get="/get-orders?page=0&order_by={column['order_by']}&order={'ASC' if t_order == 'DESC' else 'DESC'}"
                    hx-target="#replace"
                    hx-swap="innerHTML">
                    {column["name"]} {"↓" if t_order == "DESC"  else "↑"}
                </th>
        """
    return f"""
                <th class="border w-28">
                    {column["name"]}
                </th>
        """


@app.route("/get-orders", methods=["GET"])
def get_orders():
    page = int(request.args.get("page", 1))
    order_by = request.args.get("order_by", "order_id")
    t_order = request.args.get("order", "ASC")

    thead = """
                <tr hx-swap-oob="innerHTML:thead">
                    <th class="border w-10"></th>
    """

    for column in table_columns:
        if column["order_by"] == order_by:
            thead += create_th(column, t_order)
        else:
            thead += create_th(column, "DESC")

    thead += "</tr>"

    rows = """"""
    for order in db.get_orders_paged(10, page * 10, order_by, t_order):
        rows += f"""
            <tr>
            <td class="border" hx-post=/delete-order?id={order[0]}>X</td>
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
        + thead
    )


@app.route("/delete-order", methods=["POST"])
def delete_order():
    order_id = request.args.get("id")
    db.delete_order(order_id)
    return redirect(url_for("orders"))


@app.route("/add-order", methods=["POST"])
def add_order():
    customer_id = request.form["customer_id"]
    product_id = request.form["product_id"]
    store_id = request.form["store_id"]
    employee_id = request.form["employee_id"]
    order_date = request.form["order_date"]
    ship_date = request.form["ship_date"]
    required_date = request.form["required_date"]
    order_status = request.form["order_status"]
    quantity = request.form["quantity"]

    db.insert_order(
        customer_id,
        product_id,
        store_id,
        employee_id,
        order_date,
        ship_date,
        required_date,
        order_status,
        quantity,
    )
    return redirect(url_for("orders"))


@app.route("/test", methods=["GET"])
def test():
    return jsonify(db.monthly_order())
