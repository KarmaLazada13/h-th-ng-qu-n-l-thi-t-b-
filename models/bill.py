import sqlite3
from models.database import get_db_connection


class Bill:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS electric_bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                meter_reading REAL NOT NULL,
                billing_month TEXT NOT NULL,
                amount_due REAL NOT NULL,
                payment_status TEXT CHECK(payment_status IN ('Đã trả', 'Chưa trả')) NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def add_bill(customer_name, meter_reading, billing_month, amount_due, payment_status):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO electric_bills (customer_name, meter_reading, billing_month, amount_due, payment_status) 
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_name, meter_reading, billing_month, amount_due, payment_status))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_bills():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM electric_bills')
        bills = cursor.fetchall()
        conn.close()
        return bills

    @staticmethod
    def update_bill(bill_id, customer_name, meter_reading, billing_month, amount_due, payment_status):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE electric_bills 
            SET customer_name=?, meter_reading=?, billing_month=?, amount_due=?, payment_status=? 
            WHERE id=?
        ''', (customer_name, meter_reading, billing_month, amount_due, payment_status, bill_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_bill(bill_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM electric_bills WHERE id=?', (bill_id,))
        conn.commit()
        conn.close()
    