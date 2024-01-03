from flask import (
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    current_app,
    Blueprint,
)

categories_bp = Blueprint("categories_bp", __name__)

def paginate(data, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]


@categories_bp.route("/categories", methods=["GET"])
def categories():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"
    

    categories=db.select_all_categories()
    
    page = int(request.args.get('page', 1))
    per_page = 1500
    paginated_items = paginate(categories, page, per_page)

    
    return render_template('categories.html', categories=paginated_items, page=page)


@categories_bp.route("/get_categories_by_id", methods=["GET"])
def get_category_by_id():

    db = current_app.config.get("db")

    if db is None:
        return "No database found"
    
    categories_id = request.args.get('category_id')
    
    category = db.get_categories_by_id(categories_id)

    return jsonify({"category": category})


@categories_bp.route("/insert_category", methods=["GET", "POST"])
def insert_category():

    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        category_id = request.form["category_id"]
        employee_id = request.form["employee_id"]
        category_name = request.form["category_name"]
        rating = request.form["rating"]
        quantity_sold = request.form["quantity_sold"]
        being_manufactured = request.form["being_manufactured"]
        total_sold_value = request.form["total_sold_value"]

        db.insert_category(
            category_id,
            employee_id,
            category_name,
            rating,
            quantity_sold,
            being_manufactured,
            total_sold_value,
        
        )
        
        return redirect(url_for('categories_bp.categories'))
    else:
        return render_template("insert_category.html")
    

@categories_bp.route("/update_category", methods=["GET", "POST"])
def update_category():

    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        categories_id = request.form["category_id"]
        employee_id = request.form["employee_id"]
        category_name = request.form["category_name"]
        rating = request.form["rating"]
        quantity_sold = request.form["quantity_sold"]
        being_manufactured = request.form["being_manufactured"]
        total_sold_value = request.form["total_sold_value"]

        db.update_category_by_id(
            categories_id,
            employee_id,
            category_name,
            rating,
            quantity_sold,
            being_manufactured,
            total_sold_value,
        )
        return redirect(url_for('categories_bp.categories'))
    else:
        return render_template("update_category.html")
    


@categories_bp.route("/delete_category", methods=["GET","POST"])
def delete_category():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        category_id = request.form["category_id"]

        db.delete_category_by_id(category_id)

        return redirect(url_for("categories_bp.categories"))
    
    else:
        if request.args.get('category_id') is not None:
            category_id = (request.args.get('category_id'))
            db.delete_category_by_id(category_id)

        return redirect(url_for("categories_bp.categories"))