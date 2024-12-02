from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import uuid
from app.models import db, RecurringExpense


expenses_bp = Blueprint("recurring-expenses", __name__, url_prefix="/api/recurring-expenses")

@expenses_bp.route('/', methods=['POST'])
@jwt_required()
def add_expense():
    current_user = get_jwt_identity()  # Get the current logged-in user
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

@expenses_bp.route('/', methods=['GET'])
@jwt_required()
def get_expenses():
    current_user = get_jwt_identity()
    expenses = RecurringExpense.query.filter_by(user_id=current_user).all()

    if not expenses:
        return jsonify({"msg": "No recurring expenses found."}), 404

    data = [{
        "id": expense.id,
        "expense_name": expense.expense_name,
        "amount": expense.amount,
        "frequency": expense.frequency,
        "start_date": expense.start_date.strftime('%Y-%m-%d'),
        "created_at": expense.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for expense in expenses]

    return jsonify({"msg": "Recurring expenses retrieved successfully.", "data": data}), 200

@expenses_bp.route('/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    current_user = get_jwt_identity()

    expense = RecurringExpense.query.filter_by(id=expense_id, user_id=current_user).first()

    if not expense:
        return jsonify({"msg": "Expense not found."}), 404

    try:
        db.session.delete(expense)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to delete recurring expense.", "error": str(e)}), 500

    return jsonify({"msg": "Recurring expense deleted successfully."}), 200

@expenses_bp.route('/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"msg": "No data provided."}), 400

    expense = RecurringExpense.query.filter_by(id=expense_id, user_id=current_user).first()

    if not expense:
        return jsonify({"msg": "Expense not found."}), 404

    try:
        if 'expense_name' in data:
            expense.expense_name = data['expense_name']
        if 'amount' in data:
            expense.amount = data['amount']
        if 'frequency' in data:
            expense.frequency = data['frequency']
        if 'start_date' in data:
            expense.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to update recurring expense.", "error": str(e)}), 500
    
    return jsonify({"msg": "Recurring expense updated successfully.", "data": {
        "id": expense.id,
        "expense_name": expense.expense_name,
        "amount": expense.amount,
        "frequency": expense.frequency,
        "start_date": expense.start_date.strftime('%Y-%m-%d'),
        "created_at": expense.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }}), 200


@expenses_bp.route('/projection', methods=['GET'])
@jwt_required()
def projection():
    current_user = get_jwt_identity()

    expenses = RecurringExpense.query.filter_by(user_id=current_user).all()

    if not expenses:
        return jsonify({"msg": "No recurring expenses found."}), 404

    now = datetime.now()
    projection = {}

    for i in range(12):
        month = (now + timedelta(days=i * 30)).strftime('%Y-%m')
        projection[month] = 0

        for expense in expenses:
            if expense.frequency == "monthly":
                projection[month] += expense.amount

    data = [{"month": month, "total_expense": amount} for month, amount in projection.items()]

    return jsonify({"msg": "Projection generated successfully.", "data": data}), 200

