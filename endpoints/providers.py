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


@providers_bp.route("/providers")
def get_providers():
    db = current_app.config.get("db")
    searchword = request.args.get("search", "")
    searchword = "%" + searchword + "%"
    start_debt = request.args.get("from", "")
    end_debt = request.args.get("to", "")
    return render_template("providers.html", providers = db.get_providers(search=searchword, start=start_debt, to=end_debt))


@providers_bp.route("/providers/countries")
def get_proiveder_countries():
    db = current_app.config.get("db")
    return jsonify(db.get_provider_countries())
