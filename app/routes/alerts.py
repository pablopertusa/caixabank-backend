from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Alert

alerts_bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

@alerts_bp.route('/amount_reached', methods=['POST'])
@jwt_required()
def create_savings_goal_alert():
    current_user = get_jwt_identity()  # Get the current logged-in user
    data = request.get_json()

    if not data or 'target_amount' not in data or 'alert_threshold' not in data:
        return jsonify({"msg": "No empty fields allowed."}), 400

    if data['target_amount'] <= 0 or data['alert_threshold'] <= 0:
        return jsonify({"msg": "Invalid values for target amount or alert threshold."}), 400
    
    alert = Alert(
        user_id=current_user,
        target_amount=data['target_amount'],
        alert_threshold=data['alert_threshold']
    )
    
    db.session.add(alert)
    db.session.commit()

    return jsonify({
        "msg": "Correctly added savings alert!",
        "data": {
            "id": alert.id,
            "user_id": alert.user_id,
            "target_amount": alert.target_amount,
            "alert_threshold": alert.alert_threshold
        }
    }), 201

@alerts_bp.route('/balance_drop', methods=['POST'])
@jwt_required()
def create_balance_drop_alert():
    current_user = get_jwt_identity()  # Get the current logged-in user
    data = request.get_json()

    if not data or 'balance_drop_threshold' not in data:
        return jsonify({"msg": "No empty fields allowed."}), 400

    if data['balance_drop_threshold'] <= 0:
        return jsonify({"msg": "Invalid value for balance drop threshold."}), 400
    
    alert = Alert(
        user_id=current_user,
        balance_drop_threshold=data['balance_drop_threshold']
    )
    
    db.session.add(alert)
    db.session.commit()

    return jsonify({
        "msg": "Correctly added balance drop alert!",
        "data": {
            "id": alert.id,
            "user_id": alert.user_id,
            "balance_drop_threshold": alert.balance_drop_threshold
        }
    }), 201

@alerts_bp.route('/delete', methods=['POST'])
@jwt_required()
def delete_alert():
    current_user = get_jwt_identity()  # Get the current logged-in user
    data = request.get_json()

    if not data or 'alert_id' not in data:
        return jsonify({"msg": "No empty fields allowed."}), 400

    alert_id = data['alert_id']
    alert = Alert.query.filter_by(id=alert_id, user_id=current_user).first()

    if not alert:
        return jsonify({"msg": "Alert not found."}), 404

    db.session.delete(alert)
    db.session.commit()

    return jsonify({"msg": "Alert deleted successfully."}), 200

@alerts_bp.route('/list', methods=['GET'])
@jwt_required()
def list_alerts():
    current_user = get_jwt_identity()  # Get the current logged-in user

    alerts = Alert.query.filter_by(user_id=current_user).all()
    if not alerts:
        return jsonify({"msg": "No alerts found."}), 404

    alerts_data = [
        {
            "id": alert.id,
            "user_id": alert.user_id,
            "target_amount": alert.target_amount,
            "alert_threshold": alert.alert_threshold,
            "balance_drop_threshold": alert.balance_drop_threshold,
            "created_at": alert.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for alert in alerts
    ]

    return jsonify({"data": alerts_data}), 200
