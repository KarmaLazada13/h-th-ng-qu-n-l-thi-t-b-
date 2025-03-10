from flask import Flask, render_template, request, redirect, url_for
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.bill import Bill
from flask import Blueprint

bill_app = Blueprint("bill_app", __name__, template_folder="../templates")  # Thêm template_folder

@bill_app.route("/")
def index():
    try:
        bills = Bill.get_all_bills()
        print("Bills loaded:", bills)  # Kiểm tra dữ liệu
        return render_template("index.html", bills=bills)
    except Exception as e:
        print("Error:", e)  # In lỗi ra terminal
        return f"Internal Server Error: {str(e)}", 500


@bill_app.route('/add', methods=['GET', 'POST'])
def add_bill():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        meter_reading = float(request.form['meter_reading'])
        billing_month = request.form['billing_month']
        amount_due = float(request.form['amount_due'])
        payment_status = request.form['payment_status']
        
        Bill.add_bill(customer_name, meter_reading, billing_month, amount_due, payment_status)
        return redirect(url_for('index'))
    return render_template('add_bill.html')

@bill_app.route('/edit/<int:bill_id>', methods=['GET', 'POST'])
def edit_bill(bill_id):
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        meter_reading = float(request.form['meter_reading'])
        billing_month = request.form['billing_month']
        amount_due = float(request.form['amount_due'])
        payment_status = request.form['payment_status']
        
        Bill.update_bill(bill_id, customer_name, meter_reading, billing_month, amount_due, payment_status)
        return redirect(url_for('index'))
    return render_template('edit_bill.html')

@bill_app.route('/delete/<int:bill_id>')
def delete_bill(bill_id):
    Bill.delete_bill(bill_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    bill_app.run(debug=True)
