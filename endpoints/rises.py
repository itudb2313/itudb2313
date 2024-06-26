from flask import (
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    current_app,
    Blueprint,
)

rises_bp = Blueprint("rises_bp", __name__)

def paginate(data, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]

# rises endpoint to view content of rise_archive table
@rises_bp.route("/rises", methods=["GET"])
def rises():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"
    
    # Fething all rises from database
    rises=db.select_all_rises()
    topRises = db.select_top_rises()
    
    # Parsing page number parameter
    page = int(request.args.get('page', 1))
    # Number of items per page.
    per_page = 10  

    # Paginate the data
    paginated_items = paginate(rises, page, per_page)


    return render_template("rises.html", rises=paginated_items, topRises=topRises, page=page)

@rises_bp.route("/get_rise_by_id", methods=["GET"])
def get_rise_by_id():

    db = current_app.config.get("db")

    if db is None:
        return "No database found"
    
    rise_id = request.args.get('rise_id')
    
    rise = db.get_rise_by_id(rise_id)

    return jsonify({"rise": rise})

# insert_rise endpoint to insert new rise record into the rise_archive table
@rises_bp.route("/insert_rise", methods=["GET", "POST"])
def insert_rise():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        rise_id = request.form["rise_id"]
        amount_by_percent = request.form["amount_by_percent"]
        rise_date = request.form["rise_date"]
        rise_state = request.form["rise_state"]

        db.insert_rise(rise_id, amount_by_percent, rise_date, rise_state)
        return redirect(url_for("rises_bp.rises"))
    else:
        return render_template("insert_rise.html", rises=db.select_all_rises())
    

@rises_bp.route("/update_rise", methods=["GET", "POST"])
def update_rise():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        rise_id = request.form["rise_id"]
        amount_by_percent = request.form["amount_by_percent"]
        rise_date = request.form["rise_date"]
        rise_state = request.form["rise_state"]

        db.update_rise_by_id(rise_id, amount_by_percent, rise_date, rise_state)
        return redirect(url_for("rises_bp.rises"))
    else:
        return render_template("insert_rise.html", rises=db.select_all_rises())


# delete_rise endpoint to delete a rise record by rise_id
@rises_bp.route("/delete_rise", methods=["GET","POST"])
def delete_rise():
    db = current_app.config.get("db")

    if db is None:
        return "No database found"

    if request.method == "POST":
        rise_id = request.form["rise_id"]

        db.delete_rise_by_id(rise_id)

        return redirect(url_for("rises_bp.rises"))
    else:
        print("REQQQ")
        if request.args.get('rise_id') is not None:
            print("OKK")
            rise_id = request.args.get('rise_id')
            db.delete_rise_by_id(rise_id)

        return redirect(url_for("rises_bp.rises"))