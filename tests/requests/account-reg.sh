# Login
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.reg", "params": {"login": "kosyachniy", "password": "asd123"}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Mail
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.reg", "params": {"mail": "polozhev@mail.ru", "password": "asd123"}, "token": "test"}' http://localhost/api/ https://web.kosyachniy.com/api/
