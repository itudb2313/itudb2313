from flask import (
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    current_app,
    Blueprint,
)

stores_bp = Blueprint("stores_bp", __name__)


@stores_bp.route("/stores", methods=["GET"])
def stores():
    db = current_app.config.get("db")
    return render_template(
        "stores.html",
        stores=db.get_all_stores_table(),
        headers=db.get_stores_columns(),
        stores_count=db.get_stores_count(),
    )

@stores_bp.route("/stores/delete", methods=["POST"])
def delete_store():
    db = current_app.config.get("db")
    store_id = request.form.get("store_id")
    print("store_id: " + str(store_id))
    db.delete_store(store_id)
    return "Deleted"
    
@stores_bp.route("/stores/update", methods=["POST"])
def edit_store():
    db = current_app.config.get("db")
    data = request.form.get("data")[1:-1].split(",")
    print(data)
    return f"""
            <tr>
            <td>{data[0]}</td>
            <td><input class="edit" type="text" id="fname" name="fname"></td>
            <td><input class="edit" type="text" id="fname" name="fname"></td>
            <td><input class="edit" type="text" id="fname" name="fname"></td>
            <td><input class="edit" type="text" id="fname" name="fname"></td>
            <td><input class="edit" type="text" id="fname" name="fname"></td>
            <td><input class="edit" type="text" id="fname" name="fname"></td>
            <td><input class="edit" type="text" id="fname" name="fname"></td>
            <td><input class="edit" type="text" id="fname" name="fname"></td>
            <td><button class="btn btn-primary">Update</button></td>
            <td><button class="btn btn-primary">Cancel</button></td>
            </tr>"""




@stores_bp.route("/stores/insert", methods=["POST"])
def insert_store():
    db = current_app.config.get("db")
    employee_id = request.form.get("employee_id")
    store_name = request.form.get("store_name")
    phone = request.form.get("phone")
    street = request.form.get("street")
    city = request.form.get("city")
    country = request.form.get("country")
    email = request.form.get("email")
    post_code = request.form.get("post_code")
    #db.insert_store(store_name, store_address, store_country, store_city, store_phone, store_email, store_manager)
    #return redirect(url_for("stores"))
    return "OK"

@stores_bp.route("/stores_table", methods=["GET"])
def stores_table():
    db = current_app.config.get("db")
    order_opt = request.args.get("order_opt")
    page_number = request.args.get("page_number")
    stores = db.get_all_stores_table(order_opt=order_opt, page_number=page_number)
    return render_template(
        "stores_table.html", stores=stores, headers=db.get_stores_columns()
    )


