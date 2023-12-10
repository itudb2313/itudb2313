from flask import render_template, request, redirect, url_for, jsonify
from app import app, db



# rises endpoint to view content of rise_archive table
@app.route("/rises", methods=["GET"])
def rises():
    return render_template("rises.html", rises=db.select_all_rises())


# insert_rise endpoint to insert new rise record into the rise_archive table
@app.route("/insert_rise", methods=["GET", "POST"])
def insert_rise():
    if request.method == "POST":
        rise_id = request.form["rise_id"]
        amount_by_percent = request.form["amount_by_percent"]
        rise_date = request.form["rise_date"]
        rise_state = request.form["rise_state"]

        db.insert_rise(rise_id, amount_by_percent, rise_date, rise_state)
        return redirect(url_for("rises"))
    else:
        return render_template("insert_rise.html", rises=db.select_all_rises())


# delete_rise endpoint to delete a rise record by rise_id
@app.route("/delete_rise", methods=["POST"])
def delete_rise():
    if request.method == "POST":
        rise_id = request.form["rise_id"]

        db.delete_rise(rise_id)

        return redirect(url_for("rises"))