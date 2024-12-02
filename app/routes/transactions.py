from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Transaction
from datetime import datetime
from app.utils.fraud_detection import calculate_daily_avg, check_rapid_transactions, check_unusual_category, check_high_deviation
from app.models import User


transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')

@transactions_bp.route('', methods=['POST'])
@jwt_required()
def add_transaction():
    current_user = get_jwt_identity()  # Get the current logged-in user
    data = request.get_json()

    if not data:
        return jsonify({"msg": "No data provided."}), 400

    # Validate input
    if 'amount' not in data or 'category' not in data:
        return jsonify({"msg": "No empty fields allowed."}), 400

    # Set timestamp if not provided
    timestamp = datetime.now() if 'timestamp' not in data else datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
    
    # Create the transaction
    transaction = Transaction(
        user_id=current_user,
        amount=data['amount'],
        category=data['category'],
        timestamp=timestamp
    )
    
    # Check for fraud detection rules
    fraud_flags = []
    if check_high_deviation(current_user, data['amount']):
        fraud_flags.append("High Deviation from Average Spending")
    if check_unusual_category(current_user, data['category']):
        fraud_flags.append("Unusual Spending Category")
    if check_rapid_transactions(current_user, timestamp, data['amount']):
        fraud_flags.append("Rapid Transactions")

    # Flag as fraud if any rule is triggered
    transaction.fraud = bool(fraud_flags)
    
    db.session.add(transaction)

    user = User.query.filter_by(id=current_user).first()
    user.balance += data['amount']
    db.session.commit()

    return jsonify({
        "msg": "Transaction added and evaluated for fraud.",
        "data": {
            "id": transaction.id,
            "user_id": transaction.user_id,
            "amount": transaction.amount,
            "category": transaction.category,
            "timestamp": transaction.timestamp,
            "fraud": transaction.fraud
        }
    }), 201
