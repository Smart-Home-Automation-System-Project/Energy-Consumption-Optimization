from flask import Blueprint, jsonify
from models.predictions import get_predictions, get_todays_predictions, get_hourly_average

bp = Blueprint('predictions', __name__, url_prefix='/predictions')

@bp.route('/')
def get_all_predictions():
    predictions = get_predictions()
    result = [dict(p) for p in predictions]
    return jsonify(result)

@bp.route('/today')
def get_today():
    predictions = get_todays_predictions()
    result = [dict(p) for p in predictions]
    return jsonify(result)

@bp.route('/hourly')
def get_hourly():
    hourly_data = get_hourly_average()
    result = [dict(h) for h in hourly_data]
    return jsonify(result)