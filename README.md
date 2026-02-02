# Infracore-momo-sms-api
Secure REST API for MoMo SMS transaction data build in python.
# Team
Team Name: Infracore
Members: 3MoMo SMS REST API Project
Overview
This project implements a REST API for a Mobile Money SMS data processing system. The API allows clients (mobile apps, web apps) to interact securely with transaction data through standard HTTP methods.
Key Components:
XML Parser - Converts SMS transaction data from XML to JSON
REST API Server - Implements CRUD operations with authentication
DSA Module - Demonstrates search algorithm efficiency comparison
Comprehensive Documentation - Complete API reference and examples
Features
Full CRUD Operations
GET all transactions
GET single transaction by ID
POST new transaction
PUT update existing transaction
DELETE transaction
Security
HTTP Basic Authentication
Protected endpoints (401 on invalid credentials)
Detailed security analysis and recommendations
 Data Structures & Algorithms
Linear Search implementation
Dictionary Lookup (Hash Table) implementation
Performance comparison and benchmarking
Complexity analysis
Documentation
Complete API endpoint documentation
Request/Response examples
Error code reference
Security best practices
Project Structure
momo_api_project/
├── api/
│   ├── server.py           # Main REST API server
│   └── test_api.sh         # Bash script for testing endpoints
├── dsa/
│   ├── xml_parser.py       # XML to JSON parser
│   └── search_comparison.py # DSA comparison module
├── data/
│   ├── modified_sms_v2.xml # Sample transaction data (XML)
│   └── transactions.json   # Parsed transaction data (JSON)
├── docs/
│   └── api_docs.md         # Complete API documentation
├── screenshots/
│   └── (test screenshots will be placed here)
├── README.md               # This file
└── team_participation.md   # Team participation sheet
Required Python Libraries
All libraries used are part of Python's standard library:
http.server - HTTP server implementation
xml.etree.ElementTree - XML parsing
json - JSON handling
base64 - Authentication encoding
time - Performance benchmarking
Installation & Setup
Step 1: Clone/Download the Repository
# If using git
git clone <repository-url>
cd momo_api_project

# Or download and extract the ZIP file

Step 2: Verify Python Installation
python3 --version
# Should show Python 3.7 or higher

Step 3: Parse XML Data
cd dsa
python3 xml_parser.py
cd ..

This will:
Parse modified_sms_v2.xml
Create transactions.json in the data folder
Display sample transaction data
 Running the API
Valid credentials:
  - Username: admin, Password: admin123
  - Username: user, Password: user123
  - Username: developer, Password: dev123

Available endpoints:
  GET    /transactions      - List all transactions
  GET    /transactions/{id} - Get specific transaction
  POST   /transactions      - Create new transaction
  PUT    /transactions/{id} - Update transaction
  DELETE /transactions/{id} - Delete transaction

Press Ctrl+C to stop the server

The server will run on http://localhost:8000 and wait for requests.
Testing
Option 1: Using the Test Script (Recommended)
Open a new terminal window (keep the server running in the first):
cd api
chmod +x test_api.sh
./test_api.sh

This will run comprehensive tests for all endpoints including:
Successful authentication
Failed authentication (401 errors)
CRUD operations
Error handling
Option 2: Manual Testing with cURL
Test GET all transactions:
curl -X GET http://localhost:8000/transactions \
  -u admin:admin123 \
  -H "Content-Type: application/json"

Test GET single transaction:
curl -X GET http://localhost:8000/transactions/5 \
  -u admin:admin123

Test POST (create new):
curl -X POST http://localhost:8000/transactions \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Send Money",
    "amount": 7500.0,
    "sender": "+250788999000",
    "receiver": "+250788000999",
    "timestamp": "2024-01-18T16:00:00",
    "status": "Completed",
    "fee": 75.0
  }'

Test PUT (update):
curl -X PUT http://localhost:8000/transactions/3 \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 20000.0,
    "status": "Pending"
  }'

Test DELETE:
curl -X DELETE http://localhost:8000/transactions/10 \
  -u admin:admin123

Test without authentication (should return 401):
curl -X GET http://localhost:8000/transactions

Option 3: Using Postman
Import the collection or create requests manually
Set Authorization:
Type: Basic Auth
Username: admin
Password: admin123
Test each endpoint as documented in docs/api_docs.md
Screenshot Requirements
Take screenshots showing:
Successful GET with authentication (200)
Unauthorized request with wrong credentials (401)
Successful POST (201)
Successful PUT (200)
Successful DELETE (200)
Save screenshots to the screenshots/ folder
Data Structures & Algorithms
Running DSA Comparison
cd dsa
python3 search_comparison.py

This will:
Load all 25 transactions
Benchmark Linear Search vs Dictionary Lookup
Test with multiple transaction IDs
Display detailed performance metrics
Show complexity analysis
Key Insights
Linear Search:
Time Complexity: O(n)
Must check each element sequentially
Slower for large datasets
No additional memory needed
Dictionary Lookup (Hash Table):
Time Complexity: O(1) average
Direct key access via hashing
Much faster for lookups
Requires additional memory for hash table
Why Dictionary is Faster: Python's dictionary uses a hash table where each key is hashed to calculate an index, allowing direct access to values in constant time. Linear search must iterate through all elements until finding the target.
Alternative Data Structures
The DSA module also discusses:
Binary Search Tree (BST) - O(log n) for balanced trees
B-Tree - Better for disk-based storage
Trie - Useful for string-based searches.
Response Codes
Code
Meaning
200
Success
201
Created
400
Bad Request
401
Unauthorized
404
Not Found
500
Server Error

Security Considerations
Current Implementation: Basic Authentication
How it works:
Client sends credentials encoded in Base64
Server decodes and validates against stored credentials
Returns 401 if invalid
Recommended Alternatives
1. JWT (JSON Web Tokens)
Stateless authentication
Token expiration and refresh
Can include claims/permissions
 Industry standard
Flow:
1. POST /auth/login → Returns JWT
2. Include in requests: Authorization: Bearer <token>
3. Server validates signature and expiration
2. OAuth 2.0
Delegated authorization
 Third-party authentication
Scope-based permissions
 Widely adopted
3. API Keys
Simple implementation
Easy to rotate
Can be rate-limited per key

Best for:
- Server-to-server communication
- Internal APIs

Production Security Checklist
[ ] Use HTTPS/TLS for all communications
[ ] Implement token-based authentication (JWT/OAuth)
[ ] Add rate limiting
[ ] Store credentials in environment variables
[ ] Implement role-based access control (RBAC)
[ ] Add request logging and monitoring
[ ] Use password hashing (bcrypt, argon2)
[ ] Implement API versioning
[ ] Add CORS policies
[ ] Enable input validation and sanitization
Team Information
Team Members
Milliam Mukamukiza
Dedine Mukabucyana
Nada Umutoni
Assignment Deliverables Checklist
[x] XML parsing implementation
[x] REST API with CRUD endpoints
[x] Basic Authentication
[x] API Documentation
[x] DSA comparison (Linear Search vs Dictionary)
[x] Test scripts
[x] README with setup instructions
[ ] Team participation sheet (to be completed)
[ ] Screenshots of test cases (to be taken)
[ ] PDF Report (to be created)
Contributing
This is an academic project. For questions or improvements:
Review the code
Test thoroughly
Document changes
Submit for review
License
This project is created for educational purposes as part of a course assignment.
Troubleshooting
Server won't start
Check if port 8000 is already in use
Verify Python version (3.7+)
Ensure XML file exists in data folder
Authentication fails
Check credentials match those in server.py
Verify Authorization header format
Try base64 encoding: echo -n "admin:admin123" | base64
No data returned
Ensure XML was parsed (run xml_parser.py first)
Check server console for errors
Verify transactions.json was created
Tests fail
Make sure server is running
Check curl is installed
Verify test script has execute permissions
 Support
For questions about this project:
Check the documentation in docs/api_docs.md
Review the code comments
Run the test scripts
Contact the team members



