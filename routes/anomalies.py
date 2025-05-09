from flask import Blueprint, jsonify
from models.anomalies import get_recent_anomalies

anomalies_bp = Blueprint('anomalies', __name__)

@anomalies_bp.route('/api/anomalies/recent', methods=['GET'])
def get_recent():
    """Get anomalies from the past hour"""
    anomalies = get_recent_anomalies()
    return jsonify(anomalies) 