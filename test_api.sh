#!/bin/bash

echo "=========================================="
echo "API Testing - Mobile Money Transactions"
echo "=========================================="
echo ""

echo "Test 1: GET / (No Authentication)"
echo "------------------------------------------"
curl -s http://localhost:8000/ | python3 -m json.tool
echo ""
echo ""

echo "Test 2: GET /transactions/1 (Single Transaction)"
echo "------------------------------------------"
curl -s -u admin:password123 http://localhost:8000/transactions/1 | python3 -m json.tool
echo ""
echo ""

echo "Test 3: Unauthorized Request (Wrong Password)"
echo "------------------------------------------"
curl -s -u admin:wrongpassword http://localhost:8000/transactions | python3 -m json.tool
echo ""
echo ""

echo "Test 4: Missing Authorization"
echo "------------------------------------------"
curl -s http://localhost:8000/transactions | python3 -m json.tool
echo ""
echo ""

echo "Test 5: GET /transactions/stats"
echo "------------------------------------------"
curl -s -u admin:password123 http://localhost:8000/transactions/stats | python3 -m json.tool
echo ""
echo ""

echo "Test 6: POST /transactions (Create New)"
echo "------------------------------------------"
curl -s -u admin:password123 -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{"transaction_type":"PAYMENT","amount":5000,"recipient":"John Doe","balance":50000}' | python3 -m json.tool
echo ""
echo ""

echo "Test 7: PUT /transactions/1692 (Update)"
echo "------------------------------------------"
curl -s -u admin:password123 -X PUT http://localhost:8000/transactions/1692 \
  -H "Content-Type: application/json" \
  -d '{"amount":7500,"recipient":"Jane Smith"}' | python3 -m json.tool
echo ""
echo ""

echo "Test 8: DELETE /transactions/1692"
echo "------------------------------------------"
curl -s -u admin:password123 -X DELETE http://localhost:8000/transactions/1692 | python3 -m json.tool
echo ""
echo ""

echo "=========================================="
echo "All Tests Completed!"
echo "=========================================="
