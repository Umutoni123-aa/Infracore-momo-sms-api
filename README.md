# Infracore-momo-sms-api
Secure REST API for MoMo SMS transaction data build in python.
# Team
Team Name: Infracore

Team-Participation-Sheet: http://docs.google.com/spreadsheets/d/1mzhwXmAXg16k03Bf7wGJuip6tBKJe7QXxIZYxel0nfk/edit?gid=0#gid=0

Mobile Money Transaction REST API 
A secure REST API for managing mobile money transaction data from SMS records.
Key Features:
Full CRUD operations (GET, POST, PUT, DELETE)

Basic Authentication for secure access

XML to JSON parsing

DSA performance comparison (Linear Search vs Dictionary Lookup)

Quick Setup
Prerequisites: Python 3.7
Installation Steps:
bash
# 1. Clone repository
git clone https://github.com/Umutoni123-aa/Infracore-momo-sms-api.git

cd Infracore-momo-sms-api

# 2. Start server
cd api
python server.py
Server runs on http://localhost:8000

Authentication
All endpoints require Basic Authentication.

- Default Credentials:
- Username: admin | Password: password123
- Alternative Accounts:
- student:momo2024
- testuser:test123
- API Endpoints

Testing Examples
1. Get all transactions:
   
bash
curl -u admin:password123 http://localhost:8000/transactions
3. Get single transaction:

bash
curl -u admin:password123 http://localhost:8000/transactions/1
4. Test unauthorized access (should return 401):
bash
curl http://localhost:8000/transactions
5. Create new transaction:
bash
curl -u admin:password123 \
-X POST \
-H "Content-Type: application/json" \
-d '{"transaction_type":"PAYMENT","amount":5000,"recipient":"John Doe"}' \
http://localhost:8000/transactions
6. Update transaction:
bash
curl -u admin:password123 \
-X PUT \
-H "Content-Type: application/json" \
-d '{"amount":6000}' \
http://localhost:8000/transactions/1
7. Delete transaction:
bash
curl -u admin:password123 -X DELETE http://localhost:8000/transactions/1
Data Structures & Algorithms
Run DSA Tests:
bash
# Test Linear Search
python dsa/linear_search.py

# Test Dictionary Lookup
python dsa/dict_lookup.py

# Compare Efficiency
python dsa/efficiency_test.py
Performance Comparison:
Algorithm
Time Complexity
Comparisons (1000 items)
Linear Search
O(n)
Up to 1,000
Dictionary Lookup
O(1)
Always 1

Why Dictionary Lookup is Faster:
Linear search checks each item sequentially (O(n))
Dictionary uses hash table for direct access (O(1))
Security Analysis
Basic Authentication Limitations:
Base64 encoding is NOT encryption
Credentials sent with every request
No protection against replay attacks
No session management or logout
Recommended Alternatives:
1. JWT (JSON Web Tokens)
Stateless authentication
Token expiration
Role-based access control
2. OAuth 2.0
Industry standard
Third-party authentication
Better for production apps
3. API Keys
Single token per client
Easy rotation/revocation
Different permission levels
4. HTTPS/TLS
Minimum requirement
Encrypts data in transit
Prevents man-in-the-middle attacks
Transaction Types
RECEIVED - Money received
PAYMENT - Merchant/agent payment
TRANSFER - Money sent to another user
DEPOSIT - Bank/cash deposit
WITHDRAWAL - Cash withdrawal
AIRTIME - Airtime/utility purchase
MERCHANT_PAYMENT - Direct payment
OTP - One-time password SMS
Team Information
Team Name: Infra Core
Members:
Dedine Mukabucyana (d.mukabucya@alustudent.com)
Nada Umutoni (u.nada@alustudent.com)
Milliam Mukamukiza (m.mukamukiz@alustudent.com)
Assignment: Building and Securing a REST API
Submission Date: 2 Feb 2026
Additional Resources
Full API Documentation: docs/api_docs.md
DSA Analysis: Run python dsa/efficiency_test.py
GitHub Repository: https://github.com/Umutoni123-aa/Infracore-momo-sms-api
Testing Guide: See API docs for comprehensive curl examples
License & Acknowledgments
This project is for educational purposes as part of a course assignment.
Data Source: Mobile Money SMS data from MTN Rwanda
Course: REST API Development and Security

