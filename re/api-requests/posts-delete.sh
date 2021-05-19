curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "posts.delete", "params": {"id": 1}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/
