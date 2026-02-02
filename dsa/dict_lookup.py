"""
Dictionary Lookup Implementation
Uses a dictionary (hash map) for fast O(1) transaction lookup by ID
"""

def build_transaction_dict(transactions):
    """
    Convert a list of transactions into a dictionary for fast lookup
    Key = transaction ID, Value = transaction data
    
    Args:
        transactions (list): List of transaction dictionaries
    
    Returns:
        dict: Dictionary with transaction IDs as keys
    """
    transaction_dict = {}
    
    for transaction in transactions:
        trans_id = transaction['id']
        transaction_dict[trans_id] = transaction
    
    return transaction_dict


def dict_lookup(transaction_dict, target_id):
    """
    Search for a transaction by ID using dictionary lookup
    This is much faster than linear search - O(1) vs O(n)
    
    Args:
        transaction_dict (dict): Dictionary of transactions
        target_id (int): The transaction ID to search for
    
    Returns:
        dict: The transaction if found, None otherwise
    """
    # Direct lookup - very fast!
    return transaction_dict.get(target_id)


def dict_lookup_with_count(transaction_dict, target_id):
    """
    Dictionary lookup that returns comparison count
    (Always 1 for hash table lookup)
    
    Args:
        transaction_dict (dict): Dictionary of transactions
        target_id (int): The transaction ID to search for
    
    Returns:
        tuple: (transaction, comparison_count)
    """
    # Dictionary lookup is always 1 comparison (hash table magic!)
    comparisons = 1
    result = transaction_dict.get(target_id)
    return result, comparisons


# Test the dictionary lookup
if __name__ == "__main__":
    # Sample test data
    test_transactions = [
        {"id": 1, "type": "RECEIVED", "amount": 2000},
        {"id": 2, "type": "PAYMENT", "amount": 1000},
        {"id": 3, "type": "TRANSFER", "amount": 500},
        {"id": 4, "type": "DEPOSIT", "amount": 5000},
        {"id": 5, "type": "PAYMENT", "amount": 300},
    ]
    
    print("Dictionary Lookup Test")
    print("*" * 50)
    
    # Build the dictionary
    trans_dict = build_transaction_dict(test_transactions)
    print(f"Built dictionary with {len(trans_dict)} transactions\n")
    
    # Test search for existing ID
    target = 4
    result = dict_lookup(trans_dict, target)
    
    if result:
        print(f"Found transaction {target}: {result}")
    else:
        print(f" Transaction {target} not found")
    
    # Test with comparison count
    target = 5
    result, count = dict_lookup_with_count(trans_dict, target)
    print(f"\nFound transaction {target} after {count} comparison (O(1)!)")
    
    # Test search for non-existing ID
    target = 99
    result = dict_lookup(trans_dict, target)
    print(f"\nSearching for transaction {target}:")
    if result:
        print(f" Found: {result}")
    else:
        print(f" Not found")
    
    print("\n" + "*" * 50)
    print("Why is dictionary lookup faster?")
    print("*" * 50)
    print("Linear Search: Checks each item one by one - O(n)")
    print("Dictionary Lookup: Uses hash table - direct access - O(1)")
    print("\nFor 1000 transactions:")
    print("  Linear: Up to 1000 comparisons")
    print("  Dictionary: Always 1 comparison!")
