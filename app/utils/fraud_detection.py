import numpy as np
from datetime import timedelta, datetime
from app.models import Transaction

def check_high_deviation(user_id, transaction_amount):
    # Get the last 90 days of transactions
    date_90_days_ago = datetime.now() - timedelta(days=90)
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.timestamp >= date_90_days_ago
    ).all()
    
    if not transactions:
        return False
    
    # Calculate average and standard deviation of daily spend
    daily_spends = {}
    for transaction in transactions:
        day = transaction.timestamp.date()
        if day not in daily_spends:
            daily_spends[day] = []
        daily_spends[day].append(transaction.amount)

    daily_avg = np.mean([np.mean(spends) for spends in daily_spends.values()])
    daily_std = np.std([np.mean(spends) for spends in daily_spends.values()])
    
    # Check if the transaction is more than 3 std devs from the average
    if abs(transaction_amount - daily_avg) > 3 * daily_std:
        return True
    return False

def check_unusual_category(user_id, transaction_category):
    # Get the last 6 months of transactions
    date_6_months_ago = datetime.now() - timedelta(days=180)
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.timestamp >= date_6_months_ago
    ).all()

    used_categories = {transaction.category for transaction in transactions}
    
    if transaction_category not in used_categories:
        return True
    return False

def check_rapid_transactions(user_id, transaction_time, transaction_amount):
    # Get transactions in the last 5 minutes
    time_window_start = transaction_time - timedelta(minutes=5)
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.timestamp >= time_window_start
    ).all()
    
    if len(transactions) > 3 and sum([t.amount for t in transactions]) + transaction_amount > calculate_daily_avg(user_id):
        return True
    return False

def calculate_daily_avg(user_id):
    # Calculate daily average for the user (all time or last 90 days)
    date_90_days_ago = datetime.now() - timedelta(days=90)
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.timestamp >= date_90_days_ago
    ).all()
    
    daily_spends = {}
    for transaction in transactions:
        day = transaction.timestamp.date()
        if day not in daily_spends:
            daily_spends[day] = []
        daily_spends[day].append(transaction.amount)

    return np.mean([np.mean(spends) for spends in daily_spends.values()])

