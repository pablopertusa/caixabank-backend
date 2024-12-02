from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import datetime
import uuid
from app.models import db, RecurringExpense


expenses_bp = Blueprint("recurring-expenses", __name__, url_prefix="/api/recurring-expenses")

@expenses_bp.route('/', methods=['POST'])
@jwt_required()
def add_expense():
    current_user = get_jwt_identity()  # Get the current logged-in user
    print(current_user)
    data = request.get_json()

    if not data or 'expense_name' not in data or 'amount' not in data or 'frequency' not in data or 'start_date' not in data:
        return jsonify({"msg": "No data provided."}), 400
    
    # Ensure fields are not empty
    if any(not data[field] for field in ['expense_name', 'amount', 'frequency', 'start_date']):
        return jsonify({"msg": "No empty fields allowed."}), 400
    
    try:
        # Convert start_date to datetime object
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"msg": "Invalid date format."}), 400
    
    # Generate unique ID for the expense
    expense_id = str(uuid.uuid4())
    print(expense_id)

    expense = {
        'id': expense_id,
        'expense_name': data['expense_name'],
        'amount': data['amount'],
        'frequency': data['frequency'],
        'start_date': start_date
    }

    new_expense = RecurringExpense(
        user_id=current_user,  # user_id should be the current user's ID (from JWT)
        expense_name=data['expense_name'],
        amount=data['amount'],
        frequency=data['frequency'],
        start_date=start_date,
        created_at=datetime.now()  # set the creation time
    )

    try:
        # Add the expense to the database
        db.session.add(new_expense)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback if any error occurs
        return jsonify({"msg": "Failed to add recurring expense.", "error": str(e)}), 500

    # Return a success response
    return jsonify({"msg": "Recurring expense added successfully.", "data": {
        "id": new_expense.id,
        "expense_name": new_expense.expense_name,
        "amount": new_expense.amount,
        "frequency": new_expense.frequency,
        "start_date": new_expense.start_date.strftime('%Y-%m-%d'),
        "created_at": new_expense.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }}), 201