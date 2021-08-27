# Server set up
1. Install NGINX (if not done)
```
sudo apt-get update
sudo apt install nginx
```

2. Customize NGINX for your project

Take [`docker/server/nginx.server.conf`](docker/server/nginx.server.conf) as a basis and add configuration:
```
sudo nano /etc/nginx/sites-enabled/<your project name>.conf
```

3. Configure NGINX

Change lines in ` /etc/nginx/nginx.conf `:
```
types_hash_max_size 20480;
client_max_body_size 30m;
```

4. Restart NGINX
```
sudo systemctl restart nginx
```

5. Set up encryption (if not done)
```
sudo snap install core; sudo snap refresh core
sudo apt-get remove certbot
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

6. Configure encryption
```
sudo certbot --nginx
```
