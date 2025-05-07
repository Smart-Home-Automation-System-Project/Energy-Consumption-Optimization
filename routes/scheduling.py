from flask import Blueprint, jsonify, request, redirect, url_for, flash, render_template
from models.scheduling import get_scheduled_tasks, get_available_devices, schedule_task
from datetime import datetime, timedelta

bp = Blueprint('scheduling', __name__, url_prefix='/scheduling')


@bp.route('/')
def get_all_tasks():
    tasks = get_scheduled_tasks()
    result = [dict(t) for t in tasks]
    return jsonify(result)


@bp.route('/devices')
def get_devices():
    devices = get_available_devices()
    result = [dict(d) for d in devices]
    return jsonify(result)


@bp.route('/schedule', methods=['POST'])
def add_task():
    data = request.form
    switch_id = data.get('device')
    target_date = data.get('date')

    if not switch_id or not target_date:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    try:
        success = schedule_task(switch_id, target_date)
        if success:
            return jsonify({'status': 'success', 'message': 'Task scheduled successfully!'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to schedule task'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500