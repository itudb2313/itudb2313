from flask import (
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    current_app,
    Blueprint,
)

providers_bp = Blueprint("providers_bp", __name__)


@providers_bp.route("/providers", methods=["GET", "POST"])
def get_providers():
    db = current_app.config.get("db")
    if request.method == "GET":
        return render_template("providers.html", providers = db.get_providers(), countries = db.get_provider_countries(), cities = db.get_provider_cities())
    elif request.method == "POST":
        searchword = "%" + request.form["search"] + "%"
        country = "%" + request.form["country"] + "%"
        city = "%" + request.form["city"] + "%"
        if request.form["min_debt"] == "":
            min_debt = 0
        else:
            min_debt = int(request.form["min_debt"])
        if request.form["max_debt"] == "":
            max_debt = 10000000000
        else:
            max_debt = int(request.form["max_debt"])
        return jsonify(db.get_providers(search=searchword, start=min_debt, to=max_debt, country=country, city=city))


@providers_bp.route("/providers/countries")
def get_proiveder_countries():
    db = current_app.config.get("db")
    return jsonify(db.get_provider_countries())

@providers_bp.route("/providers/insert", methods=["GET", "POST"])
def insert_provider():
    db = current_app.config.get("db")
    if request.method == "GET":
        return render_template("insert_provider.html")
    elif request.method == "POST":
        name = request.form["provider_name"]
        email = request.form["email"]
        country = request.form["country"]
        city = request.form["city"]
        debt = request.form["debt"]
        db.insert_provider(name, email, country, city, debt)
        return redirect(url_for("providers_bp.get_providers"))

@providers_bp.route("/providers/delete", methods=["POST"])
def delete_provider():
    db = current_app.config.get("db")
    provider_id = request.json.get("provider_id")
    try:
        db.delete_provider(provider_id)
        return ["Success"]
    except:
        return ["Error"]

@providers_bp.route("/providers/update", methods=["GET", "POST"])
def update_provider():
    db = current_app.config.get("db")
    provider_id = request.args.get("provider_id")
    if request.method == "GET":
        return render_template("update_provider.html", provider=db.get_provider(provider_id))
    else:
        name = request.form["provider_name"]
        email = request.form["email"]
        country = request.form["country"]
        city = request.form["city"]
        debt = request.form["debt"]
        db.update_provider(provider_id, name, email, country, city, debt)
        return redirect(url_for("providers_bp.get_providers"))