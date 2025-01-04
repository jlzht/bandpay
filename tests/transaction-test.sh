#!/bin/bash

API_BASE_URL="http://localhost:8000"

USER_ID=12345678
USER_NAME="Mohammed Francisco"
USER_STATUS="active"

echo "Creating user..."
curl -X POST "$API_BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{"id": '"$USER_ID"', "name": "'"$USER_NAME"'", "status": "'"$USER_STATUS"'"}' 

echo "\nUser created."

TRANSACTION_TYPE="credit"
AMOUNT=100.0
echo "Creating transaction..."
curl -X POST "$API_BASE_URL/transactions/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": '"$USER_ID"', "amount": '"$AMOUNT"', "opt": "'"$TRANSACTION_TYPE"'"}' 

echo "\nTransaction created."

echo "Getting user info..."
curl -X GET "$API_BASE_URL/users/$USER_ID/" -H "Content-Type: application/json"
echo "\n"
