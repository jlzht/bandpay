# simple shell script
curl -X 'POST' 'http://127.0.0.1:8000/users/' \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 2001,
    "name": "John Doe",
    "status": "poig"
  }'
