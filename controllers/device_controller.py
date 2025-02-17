from models.device import Device
def add_device(device_name, device_type, brand, location, status):
    device = Device(device_name, device_type, brand, location, status)
    device.save()

def update_device(device_id, device_name, device_type, brand, location, status):
    Device.update(device_id, device_name, device_type, brand, location, status)

def delete_device(device_id):
    Device.delete(device_id)

def get_all_devices():
    return Device.get_all()

def get_device_by_id(device_id):
    return Device.get_by_id(device_id)

def search_devices(keyword):
    return Device.search(keyword)

