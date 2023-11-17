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

    rows = ''''''
    for order in db.get_orders_paged(10,page*10):
        rows += f'''
            <tr>
            <td>{order[0]}</td>
            <td>{order[1]}</td>
            <td>{order[2]}</td>
            <td>{order[3]}</td>
            <td>{order[4]}</td>
            <td>{order[5]}</td>
            <td>{order[6]}</td>
            <td>{order[7]}</td>
            <td>{order[8]}</td>
            <td>{order[9]}</td>
        </tr>'''

    return rows + f'<tr><td colspan="10" hx-get="/htmx-test?page={page+1}" hx-target="#replace" hx-swap="innerHTML">click for next page: {page+1}</td></tr>'


app.run()
