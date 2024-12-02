from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd

# Load CSV files into DataFrames
exchange_rates_df = pd.read_csv('app/exchange_rates.csv')
exchange_fees_df = pd.read_csv('app/exchange_fees.csv')

transfers_bp = Blueprint('transfers', __name__, url_prefix='/api/transfers')

# Simulate Transfer
@transfers_bp.route('/simulate', methods=['POST'])
@jwt_required()
def simulate_transfer():
    current_user = get_jwt_identity()  # Ensure the user is authenticated
    data = request.get_json()

    if not data or 'amount' not in data or 'source_currency' not in data or 'target_currency' not in data:
        return jsonify({"msg": "No empty fields allowed."}), 400

    amount = data['amount']
    source_currency = data['source_currency']
    target_currency = data['target_currency']

    # Get the exchange rate from the DataFrame
    exchange_rate_row = exchange_rates_df[(exchange_rates_df['currency_from'] == source_currency) &
                                          (exchange_rates_df['currency_to'] == target_currency)]
    
    if exchange_rate_row.empty:
        return jsonify({"msg": "Invalid currencies or no exchange data available."}), 404
    
    rate = exchange_rate_row.iloc[0]['rate']

    # Get the exchange fee from the DataFrame
    exchange_fee_row = exchange_fees_df[(exchange_fees_df['currency_from'] == source_currency) &
                                        (exchange_fees_df['currency_to'] == target_currency)]
    
    if exchange_fee_row.empty:
        return jsonify({"msg": "No fee information available for these currencies."}), 404
    
    fee = exchange_fee_row.iloc[0]['fee']

    # Calculate the amount the recipient will receive
    target_amount = amount * (1 - fee) * rate

    return jsonify({"msg": f"Amount in target currency: {target_amount:.2f}."}), 201

# Get Fees
@transfers_bp.route('/fees', methods=['GET'])
@jwt_required()
def get_fees():
    source_currency = request.args.get('source_currency')
    target_currency = request.args.get('target_currency')

    if not source_currency or not target_currency:
        return jsonify({"msg": "No empty fields allowed."}), 400

    # Get the fee from the DataFrame
    fee_row = exchange_fees_df[(exchange_fees_df['currency_from'] == source_currency) &
                                (exchange_fees_df['currency_to'] == target_currency)]
    
    if fee_row.empty:
        return jsonify({"msg": "No fee information available for these currencies."}), 404

    fee = fee_row.iloc[0]['fee']

    return jsonify({"fee": fee}), 200

# Get Exchange Rates
@transfers_bp.route('/rates', methods=['GET'])
@jwt_required()
def get_exchange_rate():
    source_currency = request.args.get('source_currency')
    target_currency = request.args.get('target_currency')

    if not source_currency or not target_currency:
        return jsonify({"msg": "No empty fields allowed."}), 400

    # Get the exchange rate from the DataFrame
    rate_row = exchange_rates_df[(exchange_rates_df['currency_from'] == source_currency) &
                                  (exchange_rates_df['currency_to'] == target_currency)]
    
    if rate_row.empty:
        return jsonify({"msg": "No exchange rate available for these currencies."}), 404

    rate = rate_row.iloc[0]['rate']

    return jsonify({"rate": rate}), 200
