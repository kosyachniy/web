# Simple
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.exit", "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/
