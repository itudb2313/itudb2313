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

columns = ['product_id', 'product_name', 'model', 'year', 'color', 'km', 'price']

@products_bp.route("/products", methods=["GET", "POST"])
def get_products():
    db = current_app.config.get("db")
    if request.method == "POST":
        searchword = "%" + request.form["search"] + "%"
        color = "%" + request.form["color"] + "%"
        order = columns[int(request.form["order"])]
        order_type = request.form["order_type"]
        if order_type == "0":
            order = order + " ASC"
        elif order_type == "1":
            order = order + " DESC"
        if request.form["min_price"] == "":
            min_price = 0
        else:
            min_price = int(request.form["min_price"])
        if request.form["max_price"] == "":
            max_price = 10000000000
        else:
            max_price = int(request.form["max_price"])
        if request.form["min_km"] == "":
            min_km = 0
        else:
            min_km = int(request.form["min_km"])
        if request.form["max_km"] == "":
            max_km = 10000000000
        else:
            max_km = int(request.form["max_km"])
        if request.form["min_year"] == "":
            min_year = 0
        else:
            min_year = int(request.form["min_year"])
        if request.form["max_year"] == "":
            max_year = 10000000000
        else:
            max_year = int(request.form["max_year"])
        if request.form["page"] == "":
            page = 0
        else:
            page = int(request.form["page"])
        
        products = db.get_products(search=searchword, lowest_price=min_price, highest_price=max_price, lowest_km=min_km, highest_km=max_km, color=color, lowest_year=min_year, highest_year=max_year, page=page, order=order)
        return jsonify(products)
    else:
        return render_template("products.html", products=db.get_products(), colors=db.get_colors())
    
    


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
    return redirect(url_for("products_bp.get_products"))


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
        return redirect(url_for("products_bp.get_products"))
    else:
        return ["Error"]



@products_bp.route("/update_product", methods=["GET","POST"])
def update_product():
    product_id = request.args.get("product_id")
    if request.method == "GET":
        db = current_app.config.get("db")
        return render_template(
            "update_product.html",
            product=db.get_product(product_id),
            providers=db.get_providers(),
            categories=db.select_all_categories(),
        )
    elif request.method == "POST":
        db = current_app.config.get("db")
        product_name = request.form["brand"]
        model = request.form["model"]
        year = request.form["year"]
        color = request.form["color"]
        price = request.form["price"]
        km = request.form["km"]
        category_id = request.form["category_id"]
        provider_id = request.form["provider_id"]
        if db.update_product(product_id, product_name, model, year, color, price, km, category_id, provider_id):
            return redirect(url_for("products_bp.get_products"))
        else:
            return ["Error"]