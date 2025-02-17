from flask import Flask, render_template, request, redirect, url_for
from controllers.device_controller import *

app = Flask(__name__)

@app.route("/")
def index():
    devices = get_all_devices()
    return render_template("index.html", devices=devices)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        add_device(request.form["device_name"], request.form["device_type"],
                   request.form["brand"], request.form["location"], request.form["status"])
        return redirect(url_for("index"))
    return render_template("add_device.html")

@app.route("/edit/<int:device_id>", methods=["GET", "POST"])
def edit(device_id):
    device = get_device_by_id(device_id)
    if request.method == "POST":
        update_device(device_id, request.form["device_name"], request.form["device_type"],
                      request.form["brand"], request.form["location"], request.form["status"])
        return redirect(url_for("index"))
    return render_template("edit_device.html", device=device)

@app.route("/delete/<int:device_id>")
def delete(device_id):
    delete_device(device_id)
    return redirect(url_for("index"))

@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        keyword = request.form.get("keyword", "")
        results = search_devices(keyword)
    return render_template("search.html", results=results)
if __name__ == "__main__":
    app.run(debug=True)
