# Mail

curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.auth", "params": {"login": "polozhev@mail.ru", "password": "password"}}' http://localhost/api/ https://web.kosyachniy.com/api/
