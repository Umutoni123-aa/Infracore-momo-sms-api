"""
Efficiency Test - Compare Linear Search vs Dictionary Lookup
Tests both algorithms with real transaction data and measures performance
"""

import time
import sys
import os

# Add parent directory to path to import parse_xml
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parse_xml import parse_xml_file
from linear_search import linear_search_with_count
from dict_lookup import build_transaction_dict, dict_lookup_with_count


def test_search_efficiency(transactions, search_ids):
    """
    Compare efficiency of linear search vs dictionary lookup
    
    Args:
        transactions (list): List of transaction dictionaries
        search_ids (list): List of transaction IDs to search for
    """
    print("=" * 70)
    print("EFFICIENCY COMPARISON: Linear Search vs Dictionary Lookup")
    print("=" * 70)
    print(f"Total Transactions: {len(transactions)}")
    print(f"Test Searches: {len(search_ids)}")
    print("=" * 70)
    
    # Build dictionary for dict lookup
    print("\nBuilding dictionary...")
    start_time = time.time()
    trans_dict = build_transaction_dict(transactions)
    build_time = time.time() - start_time
    print(f"✓ Dictionary built in {build_time:.6f} seconds")
    
    # Test Linear Search
    print("\n--- LINEAR SEARCH ---")
    linear_comparisons = 0
    linear_found = 0
    
    start_time = time.time()
    for search_id in search_ids:
        result, comparisons = linear_search_with_count(transactions, search_id)
        linear_comparisons += comparisons
        if result:
            linear_found += 1
    linear_time = time.time() - start_time
    
    print(f"Time taken: {linear_time:.6f} seconds")
    print(f"Total comparisons: {linear_comparisons}")
    print(f"Average comparisons per search: {linear_comparisons / len(search_ids):.2f}")
    print(f"Transactions found: {linear_found}/{len(search_ids)}")
    
    # Test Dictionary Lookup
    print("\n--- DICTIONARY LOOKUP ---")
    dict_comparisons = 0
    dict_found = 0
    
    start_time = time.time()
    for search_id in search_ids:
        result, comparisons = dict_lookup_with_count(trans_dict, search_id)
        dict_comparisons += comparisons
        if result:
            dict_found += 1
    dict_time = time.time() - start_time
    
    print(f"Time taken: {dict_time:.6f} seconds")
    print(f"Total comparisons: {dict_comparisons}")
    print(f"Average comparisons per search: {dict_comparisons / len(search_ids):.2f}")
    print(f"Transactions found: {dict_found}/{len(search_ids)}")
    
    # Comparison Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    speedup = linear_time / dict_time if dict_time > 0 else 0
    comparison_reduction = ((linear_comparisons - dict_comparisons) / linear_comparisons * 100) if linear_comparisons > 0 else 0
    
    print(f"Dictionary lookup is {speedup:.2f}x FASTER than linear search")
    print(f"Comparisons reduced by {comparison_reduction:.2f}%")
    print(f"\nLinear Search: O(n) - {linear_comparisons} comparisons")
    print(f"Dictionary Lookup: O(1) - {dict_comparisons} comparisons")
    
    # Detailed comparison table
    print("\n" + "=" * 70)
    print(f"{'Metric':<30} {'Linear Search':<20} {'Dict Lookup':<20}")
    print("=" * 70)
    print(f"{'Time (seconds)':<30} {linear_time:<20.6f} {dict_time:<20.6f}")
    print(f"{'Total Comparisons':<30} {linear_comparisons:<20} {dict_comparisons:<20}")
    print(f"{'Avg Comparisons/Search':<30} {linear_comparisons/len(search_ids):<20.2f} {dict_comparisons/len(search_ids):<20.2f}")
    print(f"{'Transactions Found':<30} {linear_found:<20} {dict_found:<20}")
    print("=" * 70)


def run_efficiency_test():
    """
    Main function to run the efficiency test
    """
    # Check if XML file exists
    xml_file = "../data/modified_sms_v2.xml"
    
    if not os.path.exists(xml_file):
        print(f"✗ Error: {xml_file} not found!")
        print("Please make sure the XML file is in the project root directory.")
        return
    
    # Parse transactions
    print("Loading transactions from XML...")
    transactions = parse_xml_file(xml_file)
    
    if not transactions:
        print("✗ No transactions loaded. Cannot run test.")
        return
    
    print(f"✓ Loaded {len(transactions)} transactions\n")
    
    # Select test IDs (first 20, middle 20, last 20, and some random)
    num_transactions = len(transactions)
    
    # Get IDs from different positions
    test_ids = []
    
    # First 10
    test_ids.extend(range(1, min(11, num_transactions + 1)))
    
    # Middle 10
    middle_start = num_transactions // 2
    test_ids.extend(range(middle_start, min(middle_start + 10, num_transactions + 1)))
    
    # Last 10  
    test_ids.extend(range(max(1, num_transactions - 9), num_transactions + 1))
    
    # Some non-existing IDs to test "not found" case
    test_ids.extend([9999, 10000, 99999])
    
    print(f"Testing with {len(test_ids)} search operations...\n")
    
    # Run the efficiency test
    test_search_efficiency(transactions, test_ids)
    
    # Additional Analysis
    print("\n" + "=" * 70)
    print("WHY IS DICTIONARY LOOKUP FASTER?")
    print("=" * 70)
    print("""
Linear Search (O(n)):
- Must check each transaction one by one
- Worst case: Check ALL transactions
- Best case: Find on first try
- Average: Check half the transactions

Dictionary Lookup (O(1)):
- Uses hash table for direct access
- Always finds in constant time
- No iteration needed
- Uses more memory but MUCH faster

For 1,000 transactions:
- Linear: Up to 1,000 comparisons
- Dictionary: Always 1 comparison

That's why we use dictionaries in real APIs!
    """)


if __name__ == "__main__":
    run_efficiency_test()
