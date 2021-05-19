# Send the code

curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.phone_send", "params": {"phone": "+7 (981) 163-55-78"}, "token": "token"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Check the code

curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.phone_check", "params": {"code": "0556"}, "token": "token"}' http://localhost/api/ https://web.kosyachniy.com/api/
