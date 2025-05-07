from flask import Blueprint, jsonify, request
from models.historical_data import HistoricalData

historical_bp = Blueprint('historical', __name__, url_prefix='/historical')

@historical_bp.route('/total', methods=['GET'])
def get_total_historical():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    data = HistoricalData.get_total_consumption(start_date, end_date)
    return jsonify(data)

@historical_bp.route('/by-device', methods=['GET'])
def get_historical_by_device():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    data = HistoricalData.get_consumption_by_device(start_date, end_date)
    return jsonify(data) 