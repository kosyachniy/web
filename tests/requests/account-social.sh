# Telegram
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.social", "params": {"user": 136563129}, "network": "tg"}' http://localhost/api/ https://web.kosyachniy.com/api/
