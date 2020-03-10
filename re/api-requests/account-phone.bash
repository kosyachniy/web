# Отправить код

curl -X POST -H "Content-Type: application/json" -d '{"method": "account.phone_send", "params": {"phone": "+7 (981) 163-55-78"}, "token": "token"}' http://127.0.0.1:5000/

# Проверить код

curl -X POST -H "Content-Type: application/json" -d '{"method": "account.phone_check", "params": {"code": "0556"}, "token": "token"}' http://127.0.0.1:5000/