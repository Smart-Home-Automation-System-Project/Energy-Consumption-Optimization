from flask import Blueprint, jsonify
from models.analytics import get_power_usage_stats, get_hourly_usage_today

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/power-usage', methods=['GET'])
def get_power_usage():
    """
    Get power usage statistics including:
    - Average power usage
    - Minimum and maximum power usage
    - Daily usage in kWh
    - Device level contribution percentages
    """
    try:
        stats = get_power_usage_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@analytics_bp.route('/analytics/hourly-usage', methods=['GET'])
def get_hourly_usage():
    """
    Get hourly power usage for today
    """
    try:
        hourly_data = get_hourly_usage_today()
        return jsonify({
            'success': True,
            'data': hourly_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500