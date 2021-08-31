# All
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "posts.get", "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Multiple
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "posts.get", "params": {"id": [1, 2]}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Single
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "posts.get", "params": {"id": 1}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Search
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "posts.get", "params": {"search": "new"}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Limited number
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "posts.get", "params": {"count": 1}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Limited number with a shift
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "posts.get", "params": {"count": 1, "offset": 1}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Limited number of search results with a shift
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "posts.get", "params": {"search": "new", "count": 1, "offset": 1}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/
