from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/db/<name>")
def hello(name):
    # normally you should sanitize using escape()
    return f"Hello, {name}!"
