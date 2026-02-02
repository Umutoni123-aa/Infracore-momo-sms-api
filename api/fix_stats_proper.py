with open('routes.py', 'r') as f:
    lines = f.readlines()

# Find and replace the entire get_transaction_stats function
new_lines = []
skip = False
i = 0

while i < len(lines):
    line = lines[i]
    
    # Start of the function we want to replace
    if 'def get_transaction_stats():' in line:
        # Write the corrected function
        new_lines.append(line)  # def line
        new_lines.append('    """\n')
        new_lines.append('    GET /transactions/stats - Get statistics about transactions\n')
        new_lines.append('    Bonus endpoint for analysis\n')
        new_lines.append('\n')
        new_lines.append('    Returns:\n')
        new_lines.append('        dict: Transaction statistics\n')
        new_lines.append('    """\n')
        new_lines.append('    if not transactions_list:\n')
        new_lines.append('        return {\n')
        new_lines.append('            "status": "success",\n')
        new_lines.append('            "message": "No transactions available",\n')
        new_lines.append('            "data": {}\n')
        new_lines.append('        }\n')
        new_lines.append('\n')
        new_lines.append('    # Calculate statistics\n')
        new_lines.append('    stats = {\n')
        new_lines.append('        "total_transactions": len(transactions_list),\n')
        new_lines.append('        "transaction_types": {},\n')
        new_lines.append('        "total_amount": 0,\n')
        new_lines.append('        "total_fees": 0\n')
        new_lines.append('    }\n')
        new_lines.append('\n')
        new_lines.append('    for trans in transactions_list:\n')
        new_lines.append('        # Count by type\n')
        new_lines.append('        t_type = trans.get("type", trans.get("transaction_type", "UNKNOWN"))\n')
        new_lines.append('        stats["transaction_types"][t_type] = stats["transaction_types"].get(t_type, 0) + 1\n')
        new_lines.append('\n')
        new_lines.append('        # Sum amounts (handle None values)\n')
        new_lines.append('        amount = trans.get("amount", 0)\n')
        new_lines.append('        if amount is not None:\n')
        new_lines.append('            stats["total_amount"] += amount\n')
        new_lines.append('\n')
        new_lines.append('        # Sum fees (handle None values and missing field)\n')
        new_lines.append('        fee = trans.get("fee", 0)\n')
        new_lines.append('        if fee is not None:\n')
        new_lines.append('            stats["total_fees"] += fee\n')
        new_lines.append('\n')
        new_lines.append('    return {\n')
        new_lines.append('        "status": "success",\n')
        new_lines.append('        "data": stats\n')
        new_lines.append('    }\n')
        new_lines.append('\n')
        
        # Skip until we find the next function or end
        i += 1
        while i < len(lines):
            if lines[i].startswith('def ') or lines[i].startswith('# Initialize') or lines[i].startswith('load_transactions()'):
                break
            i += 1
        continue
    
    new_lines.append(line)
    i += 1

with open('routes.py', 'w') as f:
    f.writelines(new_lines)

print("✓ Fixed get_transaction_stats function!")
