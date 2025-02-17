import sqlite3

class Device:
    def __init__(self, device_name, device_type, brand, location, status):
        self.device_name = device_name
        self.device_type = device_type
        self.brand = brand
        self.location = location
        self.status = status

    @staticmethod
    def get_all():
        conn = sqlite3.connect("devices.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices")
        devices = cursor.fetchall()
        conn.close()
        return devices

    @staticmethod
    def get_by_id(device_id):
        conn = sqlite3.connect("devices.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE id=?", (device_id,))
        device = cursor.fetchone()
        conn.close()
        return device

    def save(self):
        conn = sqlite3.connect("devices.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO devices (device_name, device_type, brand, location, status) VALUES (?, ?, ?, ?, ?)",
                       (self.device_name, self.device_type, self.brand, self.location, self.status))
        conn.commit()
        conn.close()

    @staticmethod
    def update(device_id, device_name, device_type, brand, location, status):
        conn = sqlite3.connect("devices.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE devices SET device_name=?, device_type=?, brand=?, location=?, status=? WHERE id=?",
                       (device_name, device_type, brand, location, status, device_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(device_id):
        conn = sqlite3.connect("devices.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM devices WHERE id=?", (device_id,))
        conn.commit()
        conn.close()
        
    @staticmethod
    def search(keyword):
     conn = sqlite3.connect("devices.db")
     cursor = conn.cursor()
     query = """
     SELECT * FROM devices 
     WHERE device_name LIKE ? 
       OR device_type LIKE ? 
       OR brand LIKE ? 
       OR location LIKE ? 
       OR status LIKE ?
     """
     keyword = f"%{keyword}%"
     cursor.execute(query, (keyword, keyword, keyword, keyword, keyword))
     results = cursor.fetchall()
     conn.close()
     return results
    
