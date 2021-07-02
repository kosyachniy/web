# All
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "users.get", "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Multiple
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "users.get", "params": {"id": [1, 2]}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Single
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "users.get", "params": {"id": 1}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Search

# Limited number
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "users.get", "params": {"count": 1}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Limited number with a shift
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "users.get", "params": {"count": 1, "offset": 1}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Limited number of search results with a shift
