from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    target_amount = db.Column(db.Float, nullable=True)  # Used for amount_reached alerts
    alert_threshold = db.Column(db.Float, nullable=True)  # Used for amount_reached alerts
    balance_drop_threshold = db.Column(db.Float, nullable=True)  # Used for balance_drop alerts
    created_at = db.Column(db.DateTime, default=datetime.now)

class RecurringExpense(db.Model):
    __tablename__ = 'recurring_expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    expense_name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    fraud = db.Column(db.Boolean, default=False) 
