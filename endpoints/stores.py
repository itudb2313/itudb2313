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
    
@stores_bp.route("/stores/update", methods=["GET", "POST"])
def edit_store():
    db = current_app.config.get("db")
    if(request.method == "GET"):
        data=request.args.get("data")[1:-1].split(",")
        l=[]
        for i in data:
            l.append(i.replace("'", ''))
        return f"""
                <tr id="edit">
                <td id= "store_id_cell">{l[0]}</td>
                <td><input class="edit" type="text"   name="emp_id" value="{l[1]}"></td>
                <td><input class="edit" type="text"   name="store_name" value="{l[2]}"></td>
                <td><input class="edit" type="text"   name="phone" value="{l[3]}"></td>
                <td><input class="edit" type="text"   name="street" value="{l[4]}"></td>
                <td><input class="edit" type="text"   name="city" value="{l[5]}"></td>
                <td><input class="edit" type="text"   name="country" value="{l[6]}"></td>
                <td><input class="edit" type="text"   name="email" value="{l[7]}"></td>
                <td><input class="edit" type="text"   name="post_code" value="{l[8]}"></td>
                <td><button class="btn btn-primary" id="{l[0]}" hx-post="/stores/update" hx-include="closest tr" hx-target="#data" onclick="update_trigger(this)">Update</button></td>
                <td><button class="btn btn-primary" id="cancel-button" hx-get = "/stores_table" 
                hx-trigger="click" hx-target="#data" onclick="cancel_edit(this)">Cancel</button></td>
                </form>
                </tr>"""
    if(request.method == "POST"):
        db = current_app.config.get("db")
        store_id = request.form.get("store_id")
        employee_id = request.form.get("emp_id")
        store_name = request.form.get("store_name")
        phone = request.form.get("phone")
        street = request.form.get("street")
        city = request.form.get("city")
        country = request.form.get("country")
        email = request.form.get("email")
        post_code = request.form.get("post_code")

        db.update_store(store_id, employee_id, store_name, phone, street, city, country, email, post_code)
        order_opt = request.form.get("order_opt")
        page_number = request.form.get("page_number")
        stores = db.get_all_stores_table(order_opt=order_opt, page_number=page_number)
        return render_template("stores_table.html", 
                                stores=stores, 
                                headers=db.get_stores_columns())
        



@stores_bp.route("/stores/insert", methods=["POST"])
def insert_store():
    db = current_app.config.get("db")
    store_id = request.form.get("store_id")
    emp_id = request.form.get("emp_id")
    store_name = request.form.get("store_name")
    phone = request.form.get("phone")
    street = request.form.get("street")
    city = request.form.get("city")
    country = request.form.get("country")
    email = request.form.get("email")
    post_code = request.form.get("post_code")
    db.insert_store(emp_id, store_name, phone, street, city, country, email, post_code)
    store_id = db.get_store_by_name(store_name,country,phone,street,city,email,post_code)[0][0]
    return f"""<tr>
                    <td>{store_id}</td>
                    <td>{emp_id}</td>
                    <td>{store_name}</td>
                    <td>{phone}</td>
                    <td>{street}</td>
                    <td>{city}</td>
                    <td>{country}</td>
                    <td>{email}</td>
                    <td>{post_code}</td>
                    <td>
                        <button class="btn btn-primary" hx-post="/stores/delete" hx-vals='"store_id": "13"' hx-trigger="click" hx-target="this" hx-swap="outerHTML" onclick="delete_trigger(this)">Delete</button>
                    </td>
                    <td>
                        <button class="btn btn-primary" onclick="edit_trigger(this)">Edit</button>     
                    </td> 
                </tr>
                    """

@stores_bp.route("/stores_table", methods=["GET"])
def stores_table():
    db = current_app.config.get("db")
    order_opt = request.args.get("order_opt")
    page_number = request.args.get("page_number")
    stores = db.get_all_stores_table(order_opt=order_opt, page_number=page_number)
    return render_template(
        "stores_table.html", stores=stores, headers=db.get_stores_columns()
    )


