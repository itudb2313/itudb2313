"""
This is the main file that will be run by the server.
"""

from flask import Flask
from flask import render_template
from products import get_all_products

app = Flask(__name__)
app.config.from_envvar("FLASK_APP_SETTINGS")

@app.route("/")
def hello_world():
    """
    This is the main page of the website.
    """
    return "<p>Hello, World!</p>"

@app.route("/db/<name>")
def hello(name):
    """
    This is a page that will take a name as a parameter and return a greeting.
    
    - normally you should sanitize using escape()
    """

    return f"Hello, {name}!"

@app.route("/products")
def random():
    return render_template("products.html", products=get_all_products())
