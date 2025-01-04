#!/bin/bash

API_BASE_URL="http://localhost:8000"

USER_ID=420694206
USER_NAME="Fobarius Barr"
USER_STATUS="active"

echo -e"Creating user...\n"
curl -X POST "$API_BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{"id": '"$USER_ID"', "name": "'"$USER_NAME"'", "status": "'"$USER_STATUS"'"}'

echo -e "\nUser created."
