# Mail
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.auth", "params": {"login": "polozhev@mail.ru", "password": "password"}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/
