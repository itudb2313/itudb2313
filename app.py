from flask import Flask, render_template, request
from database import Database

app = Flask(__name__)
app.config.from_object("config")
with app.app_context():
    db = Database()

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/products")
def products():
    return render_template("products.html", products=db.get_all_products())

@app.route("/orders")
def orders():
    return render_template("orders.html", orders=db.get_orders_paged(10,0))

@app.route("/htmx-test", methods=["GET"])
def htmx_test():
    page = int(request.args.get("page", 1))
    order_by = request.args.get("order_by", "order_id")
    t_order = request.args.get("order", "ASC")

    rows = ''''''
    for order in db.get_orders_paged(10,page*10, order_by, t_order):
        rows += f'''
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
        </tr>'''

    return rows + f'''
        <tr>
            <td colspan="10"
                hx-get="/htmx-test?page={page+1}&order_by={order_by}&order={t_order}"
                hx-target="#replace"
                hx-swap="innerHTML">
                click for next page: {page+1}
            </td>
        </tr>
        '''

app.run()
