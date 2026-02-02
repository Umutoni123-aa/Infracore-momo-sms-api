"""Linear Search implementation
Searches through the transaction list one by one to find a transaction by ID
"""

def linear_search(transactions, target_id):
    """
    Search for a transaction by ID using linear search
    
    Args:
        transactions (list): List of transaction dictionaries
        target_id (int): The transaction ID to search for
    
    Returns:
        dict: The transaction if found, None otherwise
    """
    # Go through each transaction one by one
    for transaction in transactions:
        if transaction['id'] == target_id:
            return transaction
    
    # If we get here, transaction was not found
    return None


def linear_search_with_count(transactions, target_id):
    """
    Linear search that also counts how many comparisons were made
    This helps us measure efficiency
    
    Args:
        transactions (list): List of transaction dictionaries
        target_id (int): The transaction ID to search for
    
    Returns:
        tuple: (transaction, comparison_count)
    """
    comparisons = 0
    
    for transaction in transactions:
        comparisons += 1
        if transaction['id'] == target_id:
            return transaction, comparisons
    
    return None, comparisons


# Test the linear search
if __name__ == "__main__":
    # Sample test data
    test_transactions = [
        {"id": 1, "type": "RECEIVED", "amount": 2000},
        {"id": 2, "type": "PAYMENT", "amount": 1000},
        {"id": 3, "type": "TRANSFER", "amount": 500},
        {"id": 4, "type": "DEPOSIT", "amount": 5000},
        {"id": 5, "type": "PAYMENT", "amount": 300},
    ]
    
    print("Linear Search Test")
    print("=" * 50)
    
    # Test search for existing ID
    target = 4
    result = linear_search(test_transactions, target)
    
    if result:
        print(f" Found transaction {target}: {result}")
    else:
        print(f" Transaction {target} not found")
    
    # Test with comparison count
    target = 5
    result, count = linear_search_with_count(test_transactions, target)
    print(f"\n Found transaction {target} after {count} comparisons")
    
    # Test search for non-existing ID
    target = 99
    result = linear_search(test_transactions, target)
    print(f"\nSearching for transaction {target}:")
    if result:
        print(f" Found: {result}")
    else:
        print(f" Not found")
