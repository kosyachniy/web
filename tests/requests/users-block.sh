# Admin
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "users.block", "params": {"id": 2}, "token": "admin"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Authorized
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "users.block", "params": {"id": 2}, "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/
