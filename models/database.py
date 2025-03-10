import sqlite3
DATABASE = "database.db"
# Kết nối đến database (nếu chưa có sẽ tự tạo)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Trả về dữ liệu dưới dạng dictionary
    return conn
# Tạo bảng nếu chưa tồn tại
cursor.execute('''
    CREATE TABLE IF NOT EXISTS electric_bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        month TEXT NOT NULL,
        consumption REAL NOT NULL,
        total_amount REAL NOT NULL
    )
''')

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Database and table created successfully!")
