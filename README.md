# Template full stack application
[![Build Status](https://app.travis-ci.com/kosyachniy/web.svg?branch=main)](https://app.travis-ci.com/kosyachniy/web)

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
            <td rowspan="3" align="center">DevOps</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/docker_logo.png?raw=true" alt="Docker" height="70" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/docker_name.png?raw=true" alt="Docker" height="70" /></td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/nginx_logo.png?raw=true" alt="NGINX" height="70" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/nginx_name.png?raw=true" alt="NGINX" height="70" /></td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/letsencrypt_logo.png?raw=true" alt="Let's Encrypt" height="70" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/letsencrypt_name.png?raw=true" alt="Let's Encrypt" height="70" /></td>
        </tr>
        <tr>
            <td rowspan="3" align="center">Back-end</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/fastapi_logo.png?raw=true" alt="FastAPI" height="70" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/fastapi_name.png?raw=true" alt="FastAPI" height="70" /></td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/mongodb_logo.png?raw=true" alt="MongoDB" height="70" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/mongodb_name.png?raw=true" alt="MongoDB" height="70" /></td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/socketio_logo.png?raw=true" alt="Socket.IO" height="70" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/socketio_name.png?raw=true" alt="Socket.IO" height="70" /></td>
        </tr>
        <tr>
            <td rowspan="4" align="center">Front-end</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/reactjs_logo.png?raw=true" alt="ReactJS" height="70" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/reactjs_name.png?raw=true" alt="ReactJS" height="70" /></td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/redux_logo.png?raw=true" alt="Redux" height="70" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/redux_name.png?raw=trueg" alt="Redux" height="70" /></td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/bootstrap_logo.png?raw=true" alt="Bootstrap 4" height="70" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/bootstrap_name.png?raw=true" alt="Bootstrap 4" height="70" /></td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/ckeditor_logo.png?raw=true" alt="CKEditor 5" height="70" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/ckeditor_name.png?raw=true" alt="CKEditor 5" height="70" /></td>
        </tr>
    </tbody>
</table>

## Install & Use with Docker
### Development
1. Customize file ` docker/.env ` & ` Makefile `

2. Run
```
make run
```

3. Open ` http://localhost/ `

### Production (dedicated server)
1. Customize file ` docker/.env ` & ` Makefile `

2. Create encryption keys
```
cd docker/
chmod 777 cert.sh
./cert.sh
```

3. Run Docker Compose
```
docker-compose -f docker-compose.alone.yml -p web up --build
```
(your project name instead of ` web `)

4. Open ` https://web.kosyachniy.com/ ` (your link)

### Production (with multiple projects)
1. Customize files ` docker/.env ` & ` Makefile `

2. Run Docker Compose
```
cd docker/
docker-compose -f docker-compose.prod.yml -p web up --build
```
(your project name instead of ` web `)

3. Set up NGINX using [docker/server/nginx.server.conf](docker/server/nginx.server.conf) (if not done)

More: [Server set up](SERVER.md)

4. Open ` https://web.kosyachniy.com/ ` (your link)

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
