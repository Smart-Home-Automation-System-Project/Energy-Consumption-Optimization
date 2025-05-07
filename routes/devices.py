from flask import Blueprint, jsonify, request
from models.devices import get_devices, get_device_by_id

devices_bp=Blueprint('devices',__name__,url_prefix='/devices')

@devices_bp.route('/')
def get_all_devices():
    devices = get_devices()
    # Convert SQLite Row objects to dictionaries
    devices_list = [dict(device) for device in devices]
    
    return jsonify(devices_list)

@devices_bp.route('/<int:switch_id>')
def get_device_by_id(switch_id):
    device = get_device_by_id(switch_id)
    if device:
        return jsonify(dict(device))
    return jsonify({'error': 'Device not found'}), 404
