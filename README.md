# Template full stack application
## Description
Web-app on JS with Python JSON-RPC API

Form | Side | Stack | Language | Path
---|---|---|---|---
API | Back-end | FastAPI | Python | ``` api/ ```
Web app | Front-end | React | JavaScript | ``` web/ ```
Telegram bot | Back-end | AIOGram | Python | ``` tg/ ```
iOS | Front-end | React Native | JavaScript | planned
Android | Front-end | React Native | JavaScript | planned

### Stack
<table>
    <thead>
        <tr>
            <th>Side</th>
            <th>Logo</th>
            <th>Technology</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="3">DevOps</td>
            <td><img src="re/img/docker_logo.png" alt="Docker" height="70" /></td>
            <td><img src="re/img/docker_name.png" alt="Docker" height="70" /></td>
        </tr>
        <tr>
            <td><img src="re/img/nginx_logo.png" alt="NGINX" height="70" /></td>
            <td><img src="re/img/nginx_name.png" alt="NGINX" height="70" /></td>
        </tr>
        <tr>
            <td><img src="re/img/letsencrypt_logo.png" alt="Let's Encrypt" height="70" /></td>
            <td><img src="re/img/letsencrypt_name.png" alt="Let's Encrypt" height="70" /></td>
        </tr>
        <tr>
            <td rowspan="3">Back-end</td>
            <td><img src="re/img/fastapi_logo.png" alt="FastAPI" height="70" /></td>
            <td><img src="re/img/fastapi_name.png" alt="FastAPI" height="70" /></td>
        </tr>
        <tr>
            <td><img src="re/img/mongodb_logo.png" alt="MongoDB" height="70" /></td>
            <td><img src="re/img/mongodb_name.png" alt="MongoDB" height="70" /></td>
        </tr>
        <tr>
            <td><img src="re/img/socketio_logo.png" alt="Socket.IO" height="70" /></td>
            <td><img src="re/img/socketio_name.png" alt="Socket.IO" height="70" /></td>
        </tr>
        <tr>
            <td rowspan="4">Front-end</td>
            <td><img src="re/img/reactjs_logo.png" alt="ReactJS" height="70" /></td>
            <td><img src="re/img/reactjs_name.png" alt="ReactJS" height="70" /></td>
        </tr>
        <tr>
            <td><img src="re/img/redux_logo.png" alt="Redux" height="70" /></td>
            <td><img src="re/img/redux_name.png" alt="Redux" height="70" /></td>
        </tr>
        <tr>
            <td><img src="re/img/bootstrap_logo.png" alt="Bootstrap 4" height="70" /></td>
            <td><img src="re/img/bootstrap_name.png" alt="Bootstrap 4" height="70" /></td>
        </tr>
        <tr>
            <td><img src="re/img/ckeditor_logo.png" alt="CKEditor 5" height="70" /></td>
            <td><img src="re/img/ckeditor_name.png" alt="CKEditor 5" height="70" /></td>
        </tr>
    </tbody>
</table>

## Install & Use with Docker
### Development
1. Customize file ` docker/.env `

2. Run
```
make run
```

3. Open

Go to ` http://localhost/ `

### Production (dedicated server)
1. Customize file ` docker/.env `

2. Create encryption keys
```
cd docker/
chmod 777 cert.sh
./cert.sh
```

3. Run Docker Compose
```
docker-compose -f docker-compose.alone.yml -p <your project name> up --build
```

4. Open

Go to ` https://web.kosyachniy.com/ ` (your link)

### Production (with multiple projects)
1. Customize files ` docker/.env ` & ` docker/server/nginx.server.conf `

2. Run Docker Compose
```
cd docker/
docker-compose -f docker-compose.prod.yml -p <your project name> up --build
```

3. Set up NGINX (if not done)
```
sudo apt-get update
sudo apt install nginx
y
```

4. Configure NGINX
```
sudo cp <path to repo>/docker/server/nginx.server.conf /etc/nginx/sites-enabled/<your project name>.conf
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

7. Open

Go to ` https://web.kosyachniy.com/ ` (your link)

## Install & Use without Docker
### Back-end
1. Change folder
```
cd api/
```

2. Customize file ` sets.json `

3. Virtual environment
```
python3 -m venv env
env/bin/pip install -r requirements.txt
```

4. Run
```
env/bin/uvicorn app:app --host 0.0.0.0 --port 5000 --proxy-headers --reload
```

### Front-end
1. Change folder
```
cd web/
```

2. Customize file ` src/sets.json `

3. Virtual environment
```
npm install
```

4. Run
#### Development
```
npm start
```

#### Production
```
npm run build
serve -s build -p 3000
```
