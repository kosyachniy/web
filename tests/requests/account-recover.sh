# Login
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.recover", "params": {"login": "kosyachniy"}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Mail
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.recover", "params": {"login": "polozhev@mail.ru"}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Phone
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.recover", "params": {"login": "+7 (969) 736-67-30"}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/
