"""
API Routes - Handles all CRUD operations for transactions
GET, POST, PUT, DELETE endpoints
"""

import json
import sys
import os

# Add parent directory to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.parse_xml import parse_xml_file
from dsa.dict_lookup import build_transaction_dict


# Global storage for transactions
transactions_list = []
transactions_dict = {}
next_id = 1


def load_transactions():
    """
    Load transactions from XML file on server startup
    """
    global transactions_list, transactions_dict, next_id

    xml_file = "../data/modified_sms_v2.xml"

    if os.path.exists(xml_file):
        print("Loading transactions from XML...")
        transactions_list = parse_xml_file(xml_file)
        transactions_dict = build_transaction_dict(transactions_list)

        if transactions_list:
            next_id = max(t['id'] for t in transactions_list) + 1
            print(f"✓ Loaded {len(transactions_list)} transactions")
        else:
            print("⚠ No transactions loaded")
    else:
        print(f"⚠ Warning: {xml_file} not found. Starting with empty database.")


def get_all_transactions():
    """
    GET /transactions - Return all transactions

    Returns:
        dict: Response with all transactions
    """
    return {
        "status": "success",
        "count": len(transactions_list),
        "data": transactions_list
    }


def get_transaction_by_id(transaction_id):
    """
    GET /transactions/{id} - Get a single transaction by ID

    Args:
        transaction_id (int): The transaction ID

    Returns:
        dict: Response with transaction or error
    """
    # Use dictionary lookup for O(1) efficiency
    transaction = transactions_dict.get(transaction_id)

    if transaction:
        return {
            "status": "success",
            "data": transaction
        }
    else:
        return {
            "status": "error",
            "message": f"Transaction with ID {transaction_id} not found",
            "error_code": 404
        }


def create_transaction(new_transaction):
    """
    POST /transactions - Create a new transaction

    Args:
        new_transaction (dict): Transaction data

    Returns:
        dict: Response with created transaction
    """
    global next_id

    # Validate required fields
    required_fields = ['transaction_type', 'amount']
    for field in required_fields:
        if field not in new_transaction:
            return {
                "status": "error",
                "message": f"Missing required field: {field}",
                "error_code": 400
            }

    # Assign new ID
    new_transaction['id'] = next_id
    next_id += 1

    # Set defaults for optional fields
    new_transaction.setdefault('balance', 0)
    new_transaction.setdefault('fee', 0)
    new_transaction.setdefault('recipient', None)
    new_transaction.setdefault('sender', None)
    new_transaction.setdefault('phone_number', None)
    new_transaction.setdefault('transaction_id', None)
    new_transaction.setdefault('date', None)

    # Add to storage
    transactions_list.append(new_transaction)
    transactions_dict[new_transaction['id']] = new_transaction

    return {
        "status": "success",
        "message": "Transaction created successfully",
        "data": new_transaction
    }


def update_transaction(transaction_id, updated_data):
    """
    PUT /transactions/{id} - Update an existing transaction

    Args:
        transaction_id (int): The transaction ID
        updated_data (dict): New transaction data

    Returns:
        dict: Response with updated transaction or error
    """
    # Check if transaction exists
    transaction = transactions_dict.get(transaction_id)

    if not transaction:
        return {
            "status": "error",
            "message": f"Transaction with ID {transaction_id} not found",
            "error_code": 404
        }

    # Update fields (don't allow ID change)
    for key, value in updated_data.items():
        if key != 'id':  # Prevent ID modification
            transaction[key] = value

    # Update in both storage structures
    transactions_dict[transaction_id] = transaction

    # Update in list (find and replace)
    for i, trans in enumerate(transactions_list):
        if trans['id'] == transaction_id:
            transactions_list[i] = transaction
            break

    return {
        "status": "success",
        "message": "Transaction updated successfully",
        "data": transaction
    }


def delete_transaction(transaction_id):
    """
    DELETE /transactions/{id} - Delete a transaction

    Args:
        transaction_id (int): The transaction ID

    Returns:
        dict: Response confirming deletion or error
    """
    # Check if transaction exists
    transaction = transactions_dict.get(transaction_id)

    if not transaction:
        return {
            "status": "error",
            "message": f"Transaction with ID {transaction_id} not found",
            "error_code": 404
        }

    # Remove from dictionary
    del transactions_dict[transaction_id]

    # Remove from list
    transactions_list[:] = [t for t in transactions_list if t['id'] != transaction_id]

    return {
        "status": "success",
        "message": f"Transaction {transaction_id} deleted successfully",
        "deleted_transaction": transaction
    }


def get_transaction_stats():
    """
    GET /transactions/stats - Get statistics about transactions
    Bonus endpoint for analysis

    Returns:
        dict: Transaction statistics
    """
    if not transactions_list:
        return {
            "status": "success",
            "message": "No transactions available",
            "data": {}
        }

    # Calculate statistics
    stats = {
        "total_transactions": len(transactions_list),
        "transaction_types": {},
        "total_amount": 0,
        "total_fees": 0
    }

    for trans in transactions_list:
        # Count by type
        t_type = trans.get("type", trans.get("transaction_type", "UNKNOWN"))
        stats["transaction_types"][t_type] = stats["transaction_types"].get(t_type, 0) + 1

        # Sum amounts (handle None values)
        amount = trans.get("amount", 0)
        if amount is not None:
            stats["total_amount"] += amount

        # Sum fees (handle None values and missing field)
        fee = trans.get("fee", 0)
        if fee is not None:
            stats["total_fees"] += fee

    return {
        "status": "success",
        "data": stats
    }

# Initialize transactions on module load
load_transactions()


# Test routes
if __name__ == "__main__":
    print("Testing API Routes")
    print("=" * 60)

    # Test GET all
    print("\n1. GET all transactions")
    result = get_all_transactions()
    print(f"Status: {result['status']}")
    print(f"Count: {result['count']}")
    print(f"First transaction: {result['data'][0] if result['data'] else 'None'}")

    # Test GET by ID
    print("\n2. GET transaction by ID (ID=1)")
    result = get_transaction_by_id(1)
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print(f"Transaction: {result['data']}")

    # Test POST (create)
    print("\n3. POST - Create new transaction")
    new_trans = {
        "transaction_type": "PAYMENT",
        "amount": 5000,
        "recipient": "Test User",
        "balance": 10000
    }
    result = create_transaction(new_trans)
    print(f"Status: {result['status']}")
    print(f"Created: {result['data']}")

    # Test PUT (update)
    print("\n4. PUT - Update transaction")
    created_id = result['data']['id']
    update_data = {
        "amount": 6000,
        "recipient": "Updated User"
    }
    result = update_transaction(created_id, update_data)
    print(f"Status: {result['status']}")
    print(f"Updated: {result['data']}")

    # Test DELETE
    print("\n5. DELETE transaction")
    result = delete_transaction(created_id)
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")

    # Test stats
    print("\n6. GET transaction statistics")
    result = get_transaction_stats()
    print(f"Status: {result['status']}")
    print(f"Stats: {json.dumps(result['data'], indent=2)}")
