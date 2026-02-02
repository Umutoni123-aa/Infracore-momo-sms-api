"""
SMS XML Parser - Extracts mobile money transactions from XML file
"""

import xml.etree.ElementTree as ET
import re
import json
from datetime import datetime


def parse_transaction_body(body):
    """
    Parse the SMS body to extract transaction details
    Returns a dictionary with transaction information
    """
    transaction = {
        "transaction_type": "UNKNOWN",
        "amount": 0,
        "recipient": None,
        "sender": None,
        "phone_number": None,
        "fee": 0,
        "transaction_id": None,
        "balance": 0,
        "message": body 
    }
    
    # Detecting RECEIVED transactions
    if "You have received" in body:
        transaction["transaction_type"] = "RECEIVED"
        
        # Extract amount: "You have received 2000 Rwf"
        amount_match = re.search(r'received (\d+(?:,\d+)*) RWF', body)
        if amount_match:
            transaction["amount"] = int(amount_match.group(1).replace(',', ''))
        
        # Extract sender: "from Jane Smith (*********013)"
        sender_match = re.search(r'from ([^(]+)\s*\(', body)
        if sender_match:
            transaction["sender"] = sender_match.group(1).strip()
        
        # Extract phone (masked): "(*********013)"
        phone_match = re.search(r'\(\*+(\d+)\)', body)
        if phone_match:
            transaction["phone_number"] = "*********" + phone_match.group(1)
        
        # Extract balance: "Your new balance:2000 RWF"
        balance_match = re.search(r'balance:?\s*(\d+(?:,\d+)*)\s*RWF', body)
        if balance_match:
            transaction["balance"] = int(balance_match.group(1).replace(',', ''))
        
        # Extract transaction ID: "Financial Transaction Id: **662021700"
        txid_match = re.search(r'Transaction Id:\s*(\d+)', body)
        if txid_match:
            transaction["transaction_id"] = txid_match.group(1)
    
    # Detect PAYMENT transactions
    elif "TxId:" in body and "Your payment of" in body:
        transaction["transaction_type"] = "PAYMENT"
        
        # Extract TxId: "TxId: 73214484437"
        txid_match = re.search(r'TxId:\s*(\d+)', body)
        if txid_match:
            transaction["transaction_id"] = txid_match.group(1)
        
        # Extract amount: "Your payment of 1,000 RWF"
        amount_match = re.search(r'payment of ([\d,]+) RWF', body)
        if amount_match:
            transaction["amount"] = int(amount_match.group(1).replace(',', ''))
        
        # Extract recipient: "to Jane Smith *2845"
        recipient_match = re.search(r'to ([A-Za-z\s]+)\s+\d+', body)
        if recipient_match:
            transaction["recipient"] = recipient_match.group(1).strip()
        
        # Extract the balance
        balance_match = re.search(r'balance:\s*([\d,]+)\s*RWF', body)
        if balance_match:
            transaction["balance"] = int(balance_match.group(1).replace(',', ''))
        
        # Extract fee
        fee_match = re.search(r'Fee was ([\d,]+) RWF', body)
        if fee_match:
            transaction["fee"] = int(fee_match.group(1).replace(',', ''))
    
    # Detect TRANSFER transactions
    elif "transferred to" in body and "*165*S*" in body:
        transaction["transaction_type"] = "TRANSFER"
        
        # Extract amount: "*165*S*10000 RWF transferred"
        amount_match = re.search(r'\*165\*S\*([\d,]+) RWF', body)
        if amount_match:
            transaction["amount"] = int(amount_match.group(1).replace(',', ''))
        
        # Extract recipient: "transferred to Samuel .."
        recipient_match = re.search(r'transferred to ([^(]+)\s*\(', body)
        if recipient_match:
            transaction["recipient"] = recipient_match.group(1).strip()
        
        # Extract phone: "(2507916666**)"
        phone_match = re.search(r'\((\d+)\)', body)
        if phone_match:
            transaction["phone_number"] = phone_match.group(1)
        
        # Extract fee
        fee_match = re.search(r'Fee was:\s*([\d,]+) RWF', body)
        if fee_match:
            transaction["fee"] = int(fee_match.group(1).replace(',', ''))
        
        # Extract balance
        balance_match = re.search(r'balance:\s*([\d,]+)\s*RWF', body)
        if balance_match:
            transaction["balance"] = int(balance_match.group(1).replace(',', ''))
    
    # Detect DEPOSIT transactions
    elif "bank deposit" in body or "*113*R*" in body:
        transaction["transaction_type"] = "DEPOSIT"
        
        # Extract amount: "A bank deposit of 40000 RWF"
        amount_match = re.search(r'deposit of ([\d,]+) RWF', body)
        if amount_match:
            transaction["amount"] = int(amount_match.group(1).replace(',', ''))
        
        # Extract balance: "NEW BALANCE :40400 RWF"
        balance_match = re.search(r'BALANCE\s*:?\s*([\d,]+)\s*RWF', body)
        if balance_match:
            transaction["balance"] = int(balance_match.group(1).replace(',', ''))
        
        transaction["recipient"] = "Bank Deposit"
    
    # Detect WITHDRAWAL transactions
    elif "withdrawn" in body:
        transaction["transaction_type"] = "WITHDRAWAL"
        
        # Extract amount: "withdrawn 20000 RWF"
        amount_match = re.search(r'withdrawn ([\d,]+) RWF', body)
        if amount_match:
            transaction["amount"] = int(amount_match.group(1).replace(',', ''))
        
        # Extract agent name
        agent_match = re.search(r'Agent ([^(]+)\s*\(', body)
        if agent_match:
            transaction["recipient"] = agent_match.group(1).strip()
        
        # Extract phone
        phone_match = re.search(r'Agent [^(]+\((\d+)\)', body)
        if phone_match:
            transaction["phone_number"] = phone_match.group(1)
        
        # Extract fee
        fee_match = re.search(r'Fee paid:\s*([\d,]+) RWF', body)
        if fee_match:
            transaction["fee"] = int(fee_match.group(1).replace(',', ''))
        
        # Extract balance
        balance_match = re.search(r'balance:\s*([\d,]+)\s*RWF', body)
        if balance_match:
            transaction["balance"] = int(balance_match.group(1).replace(',', ''))
        
        # Extract transaction ID
        txid_match = re.search(r'Transaction Id:\s*(\d+)', body)
        if txid_match:
            transaction["transaction_id"] = txid_match.group(1)
    
    # Detect AIRTIME/UTILITY payments
    elif "Airtime" in body or "Cash Power" in body:
        transaction["transaction_type"] = "AIRTIME"
        
        # Extract TxId
        txid_match = re.search(r'TxId:(\d+)', body)
        if txid_match:
            transaction["transaction_id"] = txid_match.group(1)
        
        # Extract amount
        amount_match = re.search(r'payment of ([\d,]+) RWF', body)
        if amount_match:
            transaction["amount"] = int(amount_match.group(1).replace(',', ''))
        
        # Extract recipient
        if "Airtime" in body:
            transaction["recipient"] = "Airtime Purchase"
        elif "Cash Power" in body:
            transaction["recipient"] = "Electricity (Cash Power)"
        
        # Extract fee
        fee_match = re.search(r'Fee was ([\d,]+) RWF', body)
        if fee_match:
            transaction["fee"] = int(fee_match.group(1).replace(',', ''))
        
        # Extract balance
        balance_match = re.search(r'balance:\s*([\d,]+)\s*RWF', body)
        if balance_match:
            transaction["balance"] = int(balance_match.group(1).replace(',', ''))
    
    # Detect OTP messages (not financial transactions)
    elif "one-time password" in body or "OTP" in body:
        transaction["transaction_type"] = "OTP"
        transaction["recipient"] = "MTN MoMo App"
    
    # Detect DIRECT PAYMENT (merchant payments)
    elif "DIRECT PAYMENT" in body or "*164*S*" in body:
        transaction["transaction_type"] = "MERCHANT_PAYMENT"
        
        # Extract amount
        amount_match = re.search(r'transaction of ([\d,]+) RWF', body)
        if amount_match:
            transaction["amount"] = int(amount_match.group(1).replace(',', ''))
        
        # Extract merchant name
        merchant_match = re.search(r'by ([A-Z\s]+) on', body)
        if merchant_match:
            transaction["recipient"] = merchant_match.group(1).strip()
        
        # Extract balance
        balance_match = re.search(r'balance:\s*([\d,]+)\s*RWF', body)
        if balance_match:
            transaction["balance"] = int(balance_match.group(1).replace(',', ''))
        
        # Extract fee
        fee_match = re.search(r'Fee was ([\d,]+) RWF', body)
        if fee_match:
            transaction["fee"] = int(fee_match.group(1).replace(',', ''))
        
        # Extract transaction ID
        txid_match = re.search(r'Transaction Id:\s*(\d+)', body)
        if txid_match:
            transaction["transaction_id"] = txid_match.group(1)
    
    return transaction


def convert_timestamp(timestamp_str):
    """
    Convert millisecond timestamp to readable datetime
    Example: 1715351458724 -> "2024-05-10 16:30:58"
    """
    try:
        timestamp_ms = int(timestamp_str)
        timestamp_s = timestamp_ms / 1000
        dt = datetime.fromtimestamp(timestamp_s)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return None


def parse_xml_file(xml_file_path):
    """
    Parse the XML file and return a list of transaction dictionaries
    
    Args:
        xml_file_path (str): Path to the modified_sms_v2.xml file
    
    Returns:
        list: List of transaction dictionaries
    """
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        transactions = []
        transaction_id = 1
        
        # Iterate through all SMS elements
        for sms in root.findall('sms'):
            # Get attributes
            date = sms.get('date', '')
            body = sms.get('body', '')
            readable_date = sms.get('readable_date', '')
            
            # Parse the transaction details from body
            transaction_data = parse_transaction_body(body)
            
            # Build the complete transaction record
            transaction = {
                "id": transaction_id,
                "date": convert_timestamp(date) or readable_date,
                "readable_date": readable_date,
                "timestamp": date,
                **transaction_data  # Merge parsed transaction data
            }
            
            transactions.append(transaction)
            transaction_id += 1
        
        print(f"✓ Successfully parsed {len(transactions)} transactions")
        return transactions
    
    except FileNotFoundError:
        print(f"✗ Error: File '{xml_file_path}' not found")
        return []
    except ET.ParseError as e:
        print(f"✗ Error parsing XML: {e}")
        return []
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return []


def save_to_json(transactions, output_file='transactions.json'):
    """
    Save transactions to a JSON file
    
    Args:
        transactions (list): List of transaction dictionaries
        output_file (str): Output JSON file path
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(transactions, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved {len(transactions)} transactions to {output_file}")
    except Exception as e:
        print(f"✗ Error saving to JSON: {e}")


# Main execution example
if __name__ == "__main__":
    # Parse the XML file
    xml_file = "modified_sms_v2.xml"  # Make sure this file is in the same directory
    
    print("Starting XML parsing...")
    transactions = parse_xml_file(xml_file)
    
    if transactions:
        # Save to JSON file
        save_to_json(transactions)
        
        # Display sample transactions
        print("\n" + "="*60)
        print("SAMPLE TRANSACTIONS:")
        print("="*60)
        
        # Show first 5 transactions
        for trans in transactions[:5]:
            print(f"\nID: {trans['id']}")
            print(f"Type: {trans['transaction_type']}")
            print(f"Amount: {trans['amount']} RWF")
            print(f"Recipient/Sender: {trans['recipient'] or trans['sender']}")
            print(f"Date: {trans['date']}")
            print(f"Balance: {trans['balance']} RWF")
            print("-" * 60)
        
        # Summary statistics
        print("\n" + "="*60)
        print("TRANSACTION SUMMARY:")
        print("="*60)
        
        transaction_types = {}
        for trans in transactions:
            t_type = trans['transaction_type']
            transaction_types[t_type] = transaction_types.get(t_type, 0) + 1
        
        for t_type, count in transaction_types.items():
            print(f"{t_type}: {count}")
        
        print(f"\nTotal Transactions: {len(transactions)}")
