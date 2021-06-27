# Without access
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "reviews.delete", "params": {"id": 1}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# With access
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "reviews.delete", "params": {"id": 1}, "token": "admin"}' http://localhost/api/ https://web.kosyachniy.com/api/
