with open('routes.py', 'r') as f:
    content = f.read()

# Find and replace the problematic lines
old_code = """        # Sum amounts and fees
        stats['total_amount'] += trans.get('amount', 0)
        stats['total_fees'] += trans.get('fee', 0)"""

new_code = """        # Sum amounts and fees
        amount = trans.get('amount', 0)
        fee = trans.get('fee', 0)
        stats['total_amount'] += amount if amount is not None else 0
        stats['total_fees'] += fee if fee is not None else 0"""

content = content.replace(old_code, new_code)

with open('routes.py', 'w') as f:
    f.write(content)

print("✓ Fixed the stats function!")
