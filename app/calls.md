curl -X POST http://localhost:3000/api/auth/register \
-H "Content-Type: application/json" \
-d '{"email": "pablo@gmail.com", "password": "123", "name": "pablo"}'

curl -X POST http://localhost:3000/api/auth/login \
-H "Content-Type: application/json" \
-d '{"email": "pablo@gmail.com", "password": "123"}'   

curl -X POST http://localhost:3000/api/recurring-expenses/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer x" \
-d '{
  "expense_name": "TV Subscription",
  "amount": 12.99,
  "frequency": "monthly",
  "start_date": "2024-01-01"
}'

curl -X GET http://localhost:3000/api/recurring-expenses/ \
-H "Authorization: Bearer "

curl -X GET http://localhost:3000/api/recurring-expenses/ \
-H "Authorization: Bearer x"

curl -X POST "http://localhost:3000/api/transfers/simulate" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "amount": 100.0,
    "source_currency": "USD",
    "target_currency": "EUR"
}'

curl -X POST "http://localhost:3000/api/alerts/amount_reached" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "target_amount": 5000.0,
    "alert_threshold": 100.0
}'

curl -X POST "http://localhost:3000/api/alerts/balance_drop" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "balance_drop_threshold": 100.0
}'


curl -X POST "http://localhost:3000/api/alerts/delete" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{"alert_id": 1}'

curl -X GET "http://localhost:3000/api/alerts/list" \
-H "Authorization: Bearer YOUR_JWT_TOKEN"

curl -X POST "http://localhost:3000/api/transactions" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "amount": 150.50,
    "category": "electronics",
    "timestamp": "2024-11-20T10:30:00Z"
}'




