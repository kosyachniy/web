# Login
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.save", "params": {"login": "kosyachniy"}, "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Password
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.save", "params": {"password": "asd123"}, "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Avatar
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.save", "params": {"avatar": "data:image/jpeg;base64,/9j/2wCEABQQEBkSGScXFycyJh8mMi4mJiYmLj41NTU1NT5EQUFBQUFBREREREREREREREREREREREREREREREREREREREQBFRkZIBwgJhgYJjYmICY2RDYrKzZERERCNUJERERERERERERERERERERERERERERERERERERERERERERERERERP/dAAQABP/uAA5BZG9iZQBkwAAAAAH/wAARCAA5ADkDACIAAREBAhEB/8QAdQAAAgMBAQAAAAAAAAAAAAAABAUBAwYCAAEBAQEBAAAAAAAAAAAAAAAAAQACAxAAAgECBQEGBgIDAAAAAAAAAQIDABEEEiExQVEFEyJhcZEUMlKBwfAVQrHR4REBAQEBAQEBAQAAAAAAAAAAAAERMQIhQXH/2gAMAwAAARECEQA/AM/8TNKSUY77XomBJsRC0sMhEqHxC+4P7p7UtTwetH9hyPHig6LmuCrDyNTnOg/jJXYCUknbWiVRXcK2tFdt4RMPLY3DHxI34P8AulTqwNwbsdQB060dP6mWLI5Xa1e7sgX4qQrBgz34PvROGwD4yUK11B2Xn/lOs5oIgiouetantPBQYLDmyjXwDTk1m/hT9QqL/9DM5SaOwK95G4UgEfmgj6UT2eLuyf2tdQefKi7jEy1GMvlCFiSBpVKIjyWvoBlvRuFvPIqSR5WBNtwQfvx/iuoeznUMcpzHShWWKcFiiGBdbAklT++VarBzYRFz5rNuS1IIRhUASWQF0Ni1iPQDrXUsudgS2g0GXmhrnVmPlkkJAKmNSxA5PFz6cdaWZaMDllaw0G531oXuz0FMFf/RztgeRUqzQussZGZTepyg8V2pCfKBfqeKPgz22Ix3fwF1sHtzwaqikEosm1rMTSHA41lugXOOFY6n79fKmkGLw76qrK3I2rFjr59STL1xiuzsPlDxoMw2DXNUw4TNdmAvyW2tTRy5W8aXPBJ460FjFOXNiHAUHRV3ar+ud+8DYmdHtHFqo5HJ/eKrySfSfaiWVox3jrlJB7tfpHn50L38nWmbRuP/0keHwzSIGdZAWtYoyaj0NScKyta0muq+JPlHzc+1KDv7VHFQyHS4YFhl72+ut49wfXSr5ZJ2BzNITcKtzHbXr+DWerwqLRK0ysqI0wve3ijta3rb7Gg5p2whzZpBiDY3JRl/NK12Nc1Yhb9pYlzdpCSa5/kMR9ZoapqT/9k="}, "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Name & surname
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.save", "params": {"name": "Alexey", "surname": "Poloz"}, "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Phone
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.save", "params": {"phone": "+7 (969) 736-67-30"}, "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Mail
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.save", "params": {"mail": "polozhev@mail.ru"}, "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Description
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.save", "params": {"description": "Статус"}, "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Language via name
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.save", "params": {"language": "ru"}, "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Language via code
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.save", "params": {"language": 1}, "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/

# Social
curl -w "%{time_total}\n" -X POST -H "Content-Type: application/json" -d '{"method": "account.save", "params": {"social": [{"id": 2, "user": 136563129, "language": 1}]}, "token": "authorized"}' http://localhost/api/ https://web.kosyachniy.com/api/
