from flask import (
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    current_app,
    Blueprint,
)

orders_bp = Blueprint("orders_bp", __name__)

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


@orders_bp.route("/orders")
def orders():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

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


def create_update_button(id):
    return f"""
<div class="w-6 mx-auto my-2" hx-target="closest tr" hx-get="/update-order?id={ id }">
<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 16 16">
  <path fill="white" d="M2.453 9.297C1.754 9.996 1 13.703 1 14c0 .521.406 1 1 1 .297 0 4.004-.754 4.703-1.453l5.722-5.722-4.25-4.25-5.722 5.722zM12 1c-.602 0-1.449.199-2.141.891l-.284.284 4.25 4.25.284-.284A3.04 3.04 0 0 0 15 4a3 3 0 0 0-3-3z"/>
</svg>
<div>
  """


x_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns:v="https://vecta.io/nano"><path d="M18 6L6 18"/><path d="M6 6l12 12"/></svg>"""


@orders_bp.route("/get-orders", methods=["GET"])
def get_orders():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

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

    thead += "<th class='border w-10'>Update</th></tr>"

    # | order_id | customer_id | product_id | store_id | employee_id | order_date | ship_date  | required_date | order_status | quantity | firstname | lastname | product_name | store_name | firstname | lastname |

    rows = """"""
    for order in db.get_orders_paged(10, page * 10, order_by, t_order):
        rows += f"""
            <tr id="o{order[0]}">
            <td class="border" hx-post=/delete-order?id={order[0]}>{x_svg}</td>
            <td class="border">{order[0]}</td>
            <td class="border underline">
                <a href="/customer?id={order[1]}">{order[10]} {order[11]}</a>
            </td>
            <td class="border underline">
                <a href="/products?id={order[2]}">{order[12]}</a>
            </td>
            <td class="border underline">
                <a href="/stores?id={order[3]}">{order[13]}</a>
            </td>
            <td class="border underline">
                <a href="/employees?id={order[4]}">{order[14]} {order[15]}</a>
            </td>
            <td class="border">{order[5]}</td>
            <td class="border">{order[6]}</td>
            <td class="border">{order[7]}</td>
            <td class="border">{order[8]}</td>
            <td class="border">{order[9]}</td>
            <td class="border">{create_update_button(order[0])}</td>
        </tr>"""

    return (
        rows
        + f"""
        <tr>
            <td colspan="12" >
                <div class="flex justify-center gap-4">
                    <div
                    hx-get="/get-orders?page={page-1}&order_by={order_by}&order={t_order}"
                    hx-target="#replace"
                    hx-swap="innerHTML">
                    <
                    </div>
                    <div>Page {page+1}</div>
                    <div
                    hx-get="/get-orders?page={page+1}&order_by={order_by}&order={t_order}"
                    hx-target="#replace"
                    hx-swap="innerHTML">
                    >
                    </div>
                </div>
            </td>
        </tr>
        
        """
        + thead
        + create_select_element_stores("add")
        + create_select_element_products("add")
        + create_select_element_customers("add")
    )


@orders_bp.route("/delete-order", methods=["POST"])
def delete_order():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    order_id = request.args.get("id")
    db.delete_order(order_id)

    # flask redirect creates glitchy behaviour
    redirect_obj = redirect(url_for(".orders"))
    redirect_obj.status_code = 200
    redirect_obj.headers["HX-Redirect"] = url_for(".orders")
    return redirect_obj
    # return redirect(url_for(".orders"))


@orders_bp.route("/add-order", methods=["POST"])
def add_order():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

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
    return redirect(url_for(".orders"))


@orders_bp.route("/test", methods=["GET"])
def test():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    return jsonify(db.monthly_order())


@orders_bp.route("/update-order", methods=["GET", "POST"])
def update_order():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        order_id = request.form["order_id"]
        customer_id = request.form["customer_id"]
        product_id = request.form["product_id"]
        store_id = request.form["store_id"]
        employee_id = request.form["employee_id"]
        order_date = request.form["order_date"]
        ship_date = request.form["ship_date"]
        required_date = request.form["required_date"]
        order_status = request.form["order_status"]
        quantity = request.form["quantity"]

        db.update_order(
            request.args.get("id"),
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
        redirect_obj = redirect(url_for(".orders"))
        redirect_obj.status_code = 200
        redirect_obj.headers["HX-Redirect"] = url_for(".orders")
        return redirect_obj

        return redirect(url_for(".orders"))
        return f"""
        <tr hx-swap-oob="outerHTML:#o{order_id}" id="o{order_id}">
            <td class="border" hx-post=/delete-order?id={order_id}>{x_svg}</td>
            <td class="border">{order_id}</td>
            <td class="border underline">
                <a href="/customer?id={customer_id}">{customer_id}</a>
            </td>
            <td class="border underline">
                <a href="/products?id={product_id}">{product_id}</a>
            </td>
            <td class="border underline">
                <a href="/stores?id={store_id}">{store_id}</a>
            </td>
            <td class="border underline">
                <a href="/employees?id={employee_id}">{employee_id}</a>
            </td>
            <td class="border">{order_date}</td>
            <td class="border">{ship_date}</td>
            <td class="border">{required_date}</td>
            <td class="border">{order_status}</td>
            <td class="border">{quantity}</td>
            <td class="border">{create_update_button(order_id)}</td>
        </tr>
    """

    if request.method == "GET":
        order_id = request.args.get("id")

        # TODO: db.get_order(order_id) yaratıp oradaki
        # değerleri inputlara yazdırabilirsim

        return f"""
            <td/>
            <td class="border">
            {order_id}
            <input type="hidden" name="order_id" value="{order_id}" form="update">
            </td>
            <td>
            {create_select_element_customers("update")}
            </td>
            <td>
            {create_select_element_products("update")}
            </td>
            <td>
            {create_select_element_stores("update")}
            </td>
            <td>
            <select name="employee_id" form="update" id="replace_employee_update" disabled></select>
            </td>
            <td class="border">
                <input type="date" name="order_date" form="update">
            </td>
            <td class="border">
                <input type="date" name="ship_date" form="update">
            </td>
            <td class="border">
                <input type="date" name="required_date" form="update">
            </td>
            <td class="border">
                <input type="text" value="Pending" name="order_status" form="update">
            </td>
            <td class="border">
                <input type="text" value="1" name="quantity" form="update">
            </td>
            <td class="border">
                <button form="update" type="submit">Update</button>
            </td>
            """


def create_select_element(form_name):
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    store_id = request.args.get("store_id")

    res = db.get_all_employee_ids_and_names(store_id)

    replace_elm_id = "replace_employee_" + form_name

    if len(res) == 0:
        return f"""<select hx-swap-oob="outerHTML:#{replace_elm_id}" id="{replace_elm_id}" disabled></select>"""

    select = f"""<select hx-swap-oob="outerHTML:#{replace_elm_id}" name="employee_id" id="{replace_elm_id}" form={form_name}> """

    for employee in res:
        select += f"<option value='{employee[0]}'>{employee[1]} {employee[2]}</option>"
    select += "</select>"

    return select


def create_select_element_stores(form_name):
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    res = db.get_all_store_ids_and_names()

    replace_elm_id = "replace_store_" + form_name

    if len(res) == 0:
        return f"""<select hx-swap-oob="outerHTML:#{replace_elm_id}" id="{replace_elm_id}" disabled></select>"""

    if form_name == "update":
        select = f"""<select name="store_id"  form={form_name} hx-get="/employee-selection?form=update" hx-trigger="keyup, change" hx-swap="none">"""
    else:
        select = f"""<select hx-swap-oob="outerHTML:#{replace_elm_id}" name="store_id" id="{replace_elm_id}" form={form_name} hx-get="/employee-selection" hx-trigger="change" hx-swap="none">"""

    for store in res:
        select += f"<option value='{store[0]}'>{store[1]}</option>"
    select += "</select>"

    return select


def create_select_element_products(form_name):
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    res = db.get_all_product_ids_and_names()

    replace_elm_id = "replace_product_" + form_name

    if len(res) == 0:
        return f"""<select hx-swap-oob="outerHTML:#{replace_elm_id}" id="{replace_elm_id}" disabled></select>"""

    if form_name == "update":
        select = f"""<select name="product_id"  form={form_name} hx-get="/employee-selection?form=update" change" hx-swap="none">"""
    else:
        select = f"""<select hx-swap-oob="outerHTML:#{replace_elm_id}" name="product_id" id="{replace_elm_id}" form={form_name} hx-get="/employee-selection" hx-trigger="change" hx-swap="none">"""

    for product in res:
        select += f"<option value='{product[0]}'>{product[1]} {product[2]}</option>"
    select += "</select>"

    return select


def create_select_element_customers(form_name):
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    res = db.get_all_customer_ids_and_names()

    replace_elm_id = "replace_customer_" + form_name

    if len(res) == 0:
        return f"""<select hx-swap-oob="outerHTML:#{replace_elm_id}" id="{replace_elm_id}" disabled></select>"""

    if form_name == "update":
        select = f"""<select name="customer_id"  form={form_name} hx-get="/employee-selection?form=update" change" hx-swap="none">"""
    else:
        select = f"""<select hx-swap-oob="outerHTML:#{replace_elm_id}" name="customer_id" id="{replace_elm_id}" form={form_name} hx-get="/employee-selection" hx-trigger="change" hx-swap="none">"""

    for customer in res:
        select += f"<option value='{customer[0]}'>{customer[1]} {customer[2]}</option>"
    select += "</select>"

    return select


@orders_bp.route("/employee-selection", methods=["GET"])
def employee_selection():
    form = request.args.get("form")
    if form == "update":
        return create_select_element("update")
    else:
        return create_select_element("add")
