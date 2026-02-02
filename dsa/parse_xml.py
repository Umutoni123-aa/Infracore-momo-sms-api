import xml.etree.ElementTree as ET
import os
import re


def parse_xml_file(file_path):
    # Check if XML file exists
    if not os.path.exists(file_path):
        print("XML file not found")
        return []

    tree = ET.parse(file_path)
    root = tree.getroot()

    transactions = []

    for index, sms in enumerate(root.findall("sms"), start=1):
        body = sms.get("body", "").lower()

        transaction = {
            "id": index,
            "type": "unknown",
            "amount": None,
            "sender": None,
            "receiver": None,
            "timestamp": sms.get("readable_date"),
            "raw_text": sms.get("body")
        }

        if "received" in body:
            transaction["type"] = "received"

            amount = re.search(r"received\s+([\d,]+)\s+rwf", body)
            sender = re.search(r"from\s+([a-z ]+)", body)

            if amount:
                transaction["amount"] = int(amount.group(1).replace(",", ""))
            if sender:
                transaction["sender"] = sender.group(1).strip()

            transaction["receiver"] = "self"

        elif "payment of" in body or "transferred to" in body:
            transaction["type"] = "sent"

            amount = re.search(r"of\s+([\d,]+)\s+rwf", body)
            receiver = re.search(r"to\s+([a-z ]+)", body)

            if amount:
                transaction["amount"] = int(amount.group(1).replace(",", ""))
            if receiver:
                transaction["receiver"] = receiver.group(1).strip()

            transaction["sender"] = "self"

        transactions.append(transaction)

    return transactions


if __name__ == "__main__":
    data = parse_xml_file("../data/modified_sms_v2.xml")
    print("Total transactions:", len(data))
    print(data[:2])

