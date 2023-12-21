from flask import (
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    current_app,
    Blueprint,
)

products_bp = Blueprint("products_bp", __name__)


@products_bp.route("/products", methods=["GET", "POST"])
def get_products():
    db = current_app.config.get("db")
    if request.method == "POST":
        searchword = request.form["search"]
        if request.form["min_price"] == "":
            min_price = 0
        else:
            min_price = int(request.form["min_price"])
        if request.form["max_price"] == "":
            max_price = 10000000000
        else:
            max_price = int(request.form["max_price"])
        # date
        # color
        # km
        return render_template("products.html", products=db.get_products(search="%"+searchword+"%", lowest=min_price, highest=max_price), categories=db.select_all_categories())
    else:
        return render_template("products.html", products=db.get_products(), categories=db.select_all_categories())
    
    


@products_bp.route("/insert_product", methods=["GET"])
def get_insert_product_page():
    db = current_app.config.get("db")
    return render_template(
        "insert_product.html",
        providers=db.get_providers(),
        categories=db.select_all_categories(),
    )


@products_bp.route("/delete_product", methods=["POST"])
def delete_product():
    db = current_app.config.get("db")
    product_id = request.json.get("product_id")
    db.delete_product(product_id)
    return redirect(url_for("get_products"))


@products_bp.route("/insert_product", methods=["POST"])
def insert_product():
    db = current_app.config.get("db")
    product_name = request.form["name"]
    model = request.form["model"]
    year = request.form["year"]
    color = request.form["color"]
    price = request.form["price"]
    km = request.form["mileage"]
    category_id = request.form["category_id"]
    provider_id = request.form["provider_id"]
    if db.insert_product(
        product_name, model, year, color, price, km, category_id, provider_id
    ):
        return redirect(url_for("get_products"))
    else:
        return ["Error"]
