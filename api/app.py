"""
REST API Server for Mobile Money Transactions
Uses Flask to serve CRUD endpoints with Basic Authentication
"""

from flask import Flask, request, jsonify
from functools import wraps
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from routes import (
    get_all_transactions,
    get_transaction_by_id,
    create_transaction,
    update_transaction,
    delete_transaction,
    get_transaction_stats
)
from auth import authenticate

app = Flask(__name__)

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_result = authenticate(request.headers)
        if auth_result['status'] != 200:
            return jsonify({
                'error': auth_result['error'],
                'message': 'Please provide valid credentials'
            }), auth_result['status']
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    """API information endpoint - no auth required"""
    return jsonify({
        "api": "Mobile Money Transaction API",
        "version": "1.0",
        "description": "REST API for managing mobile money SMS transactions",
        "endpoints": {
            "GET /transactions": "Get all transactions",
            "GET /transactions/<id>": "Get transaction by ID",
            "POST /transactions": "Create new transaction",
            "PUT /transactions/<id>": "Update transaction",
            "DELETE /transactions/<id>": "Delete transaction",
            "GET /transactions/stats": "Get transaction statistics"
        },
        "authentication": "Basic Authentication required for all endpoints except /"
    })


@app.route('/transactions', methods=['GET'])
@require_auth
def get_transactions():
    """GET all transactions"""
    result = get_all_transactions()
    return jsonify(result), 200


@app.route('/transactions/<int:transaction_id>', methods=['GET'])
@require_auth
def get_transaction(transaction_id):
    """GET single transaction by ID"""
    result = get_transaction_by_id(transaction_id)
    status_code = result.get('error_code', 200)
    return jsonify(result), status_code


@app.route('/transactions', methods=['POST'])
@require_auth
def create_trans():
    """CREATE new transaction"""
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No JSON data provided'
        }), 400
    
    result = create_transaction(data)
    status_code = result.get('error_code', 201)
    return jsonify(result), status_code


@app.route('/transactions/<int:transaction_id>', methods=['PUT'])
@require_auth
def update_trans(transaction_id):
    """UPDATE existing transaction"""
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No JSON data provided'
        }), 400
    
    result = update_transaction(transaction_id, data)
    status_code = result.get('error_code', 200)
    return jsonify(result), status_code


@app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
@require_auth
def delete_trans(transaction_id):
    """DELETE transaction"""
    result = delete_transaction(transaction_id)
    status_code = result.get('error_code', 200)
    return jsonify(result), status_code


@app.route('/transactions/stats', methods=['GET'])
@require_auth
def get_stats():
    """GET transaction statistics"""
    result = get_transaction_stats()
    return jsonify(result), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'error_code': 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'error_code': 500
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Mobile Money Transaction API Server")
    print("=" * 60)
    print("Server starting on http://localhost:8000")
    print("Documentation: http://localhost:8000/")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print("\nTest credentials:")
    print("Username: admin")
    print("Password: password123")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8000, debug=True)
