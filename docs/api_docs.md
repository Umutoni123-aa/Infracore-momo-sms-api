Mobile Money Transaction API
============================

Base URL
--------
localhost:8000

Authentication
--------------
- All endpoints except the home `/` require **Basic Auth**
- Valid users:
  - admin / password123
  - student / momo2024
  - testuser / test123
- Include in headers: Authorization: Basic <base64(username:password)>

Endpoints
---------

1. GET /
   - Info about API
   - No authentication needed

2. GET /transactions
   - List all transactions
   - Requires authentication
   - Example: curl -u admin:password123 localhost:8000/transactions

3. GET /transactions/{id}
   - Get a single transaction by ID
   - Example: curl -u admin:password123 localhost:8000/transactions/1

4. POST /transactions
   - Create a new transaction
   - Example:
     curl -u admin:password123 -X POST localhost:8000/transactions
     -H "Content-Type: application/json"
     -d '{"transaction_type":"PAYMENT","amount":5000,"recipient":"John Doe"}'

5. PUT /transactions/{id}
   - Update transaction details
   - Example:
     curl -u admin:password123 -X PUT localhost:8000/transactions/1
     -H "Content-Type: application/json"
     -d '{"amount":7500}'

6. DELETE /transactions/{id}
   - Delete a transaction
   - Example: curl -u admin:password123 -X DELETE localhost:8000/transactions/1

7. GET /transactions/stats
   - View summary statistics
   - Example: curl -u admin:password123 localhost:8000/transactions/stats

Notes
-----
- Returns JSON responses
- Status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found
- Use Basic Auth for all endpoints except the home `/`

