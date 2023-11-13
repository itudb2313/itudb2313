from flask import Flask, render_template
from database import Database

app = Flask(__name__)
app.config.from_object("config")
with app.app_context():
    db = Database()

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/db/<name>")
def hello(name):
    return f"Hello, {name}!"

@app.route("/products")
def products():
    return render_template("products.html", products=db.get_all_products())

app.run()
