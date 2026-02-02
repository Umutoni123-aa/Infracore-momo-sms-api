# Infracore-momo-sms-api
Secure REST API for MoMo SMS transaction data build in python.
# Team
Team Name: Infracore
Members: 3

MoMo SMS REST API Project
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

Available endpoints:
  GET    /transactions      - List all transactions
  GET    /transactions/{id} - Get specific transaction
  POST   /transactions      - Create new transaction
  PUT    /transactions/{id} - Update transaction
  DELETE /transactions/{id} - Delete transaction

Press Ctrl+C to stop the server

The server will run on http://localhost:8000 and wait for requests.
Testin
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

Test DELETE:
curl -X DELETE http://localhost:8000/transactions/10 \
  -u admin:admin123

Test without authentication (should return 401):
curl -X GET http://localhost:8000/transactions

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
This is an academic project. For questions or improvements:
Review the code
Test thoroughly
Document changes
Submit for review
License

 Support
For questions about this project:
Check the documentation in docs/api_docs.md
Review the code comments
Run the test scripts
Contact the team members through these Emails: m.mukamukiz@alustudent.com




