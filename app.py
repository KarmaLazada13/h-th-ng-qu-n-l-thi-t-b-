from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

DATABASE = "electric_bills.db"

# Kết nối database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Đóng database khi ứng dụng kết thúc
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Khởi tạo database nếu chưa có
def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                electric_usage INTEGER NOT NULL,
                month TEXT NOT NULL,
                amount INTEGER NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        db.commit()

# Trang danh sách hóa đơn
@app.route("/")
def index():
    search_query = request.args.get("search", "")
    db = get_db()
    if search_query:
        query = "SELECT * FROM bills WHERE customer_name LIKE ?"
        bills = db.execute(query, ('%' + search_query + '%',)).fetchall()
    else:
        bills = db.execute("SELECT * FROM bills").fetchall()
    return render_template("index.html", bills=bills, search_query=search_query)

# Thêm hóa đơn
@app.route("/add", methods=["GET", "POST"])
def add_bill():
    db = get_db()

    if request.method == "POST":
        customer_name = request.form["customer_name"]
        electric_usage = int(request.form["electric_usage"])
        month = int(request.form["month"])  # Chuyển tháng về kiểu số nguyên
        amount = int(request.form["amount"])
        status = request.form["status"]

        db.execute("INSERT INTO bills (customer_name, electric_usage, month, amount, status) VALUES (?, ?, ?, ?, ?)",
                   (customer_name, electric_usage, month, amount, status))
        db.commit()
        return redirect(url_for("index"))

    return render_template("add_bill.html")


# Sửa hóa đơn
@app.route("/edit/<int:bill_id>", methods=["GET", "POST"])
def edit_bill(bill_id):
    db = get_db()
    bill = db.execute("SELECT * FROM bills WHERE id = ?", (bill_id,)).fetchone()
    
    if not bill:
        return "Hóa đơn không tồn tại!", 404

    if request.method == "POST":
        customer_name = request.form["customer_name"]
        electric_usage = int(request.form["electric_usage"])
        month = int(request.form["month"])  # Chuyển tháng về kiểu số nguyên
        amount = int(request.form["amount"])
        status = request.form["status"]

        db.execute("UPDATE bills SET customer_name = ?, electric_usage = ?, month = ?, amount = ?, status = ? WHERE id = ?",
                   (customer_name, electric_usage, month, amount, status, bill_id))
        db.commit()
        return redirect(url_for("index"))

    return render_template("edit_bill.html", bill=bill)

# Xóa hóa đơn
@app.route("/delete/<int:bill_id>")
def delete_bill(bill_id):
    db = get_db()
    db.execute("DELETE FROM bills WHERE id = ?", (bill_id,))
    db.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
