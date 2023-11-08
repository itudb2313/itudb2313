"""
This is the main file that will be run by the server.
"""

from flask import Flask

app = Flask(__name__)

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

@app.route("/random")
def random():
    return ""
