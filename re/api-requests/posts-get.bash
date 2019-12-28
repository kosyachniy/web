# Все посты

curl -X POST -H "Content-Type: application/json" -d '{"method": "posts.get"}' http://127.0.0.1:5000/

# Несколько постов

curl -X POST -H "Content-Type: application/json" -d '{"method": "posts.get", "params": {"id": [1, 2]}}' http://127.0.0.1:5000/

# Один пост

curl -X POST -H "Content-Type: application/json" -d '{"method": "posts.get", "params": {"id": 1}}' http://127.0.0.1:5000/