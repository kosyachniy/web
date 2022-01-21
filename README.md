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
            <th>Version</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="3" align="center">DevOps</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/docker_logo.png?raw=true" alt="Docker" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/docker_name.png?raw=true" alt="Docker" height="50" /></td>
            <td align="center">20.10.11</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/nginx_logo.png?raw=true" alt="NGINX" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/nginx_name.png?raw=true" alt="NGINX" height="50" /></td>
            <td align="center">1.21.5</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/letsencrypt_logo.png?raw=true" alt="Let's Encrypt" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/letsencrypt_name.png?raw=true" alt="Let's Encrypt" height="50" /></td>
            <td align="center"></td>
        </tr>
        <tr>
            <td rowspan="4" align="center">Back-end</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/python_logo.png?raw=true" alt="Python" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/python_name.png?raw=true" alt="Python" height="50" /></td>
            <td align="center">3.9.10</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/fastapi_logo.png?raw=true" alt="FastAPI" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/fastapi_name.png?raw=true" alt="FastAPI" height="50" /></td>
            <td align="center">0.70.1</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/mongodb_logo.png?raw=true" alt="MongoDB" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/mongodb_name.png?raw=true" alt="MongoDB" height="50" /></td>
            <td align="center">5.0.5</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/socketio_logo.png?raw=true" alt="Socket.IO" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/socketio_name.png?raw=true" alt="Socket.IO" height="50" /></td>
            <td align="center"></td>
        </tr>
        <tr>
            <td rowspan="5" align="center">Front-end</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/javascript_logo.png?raw=true" alt="JavaScript" height="50" /></td>
            <td></td>
            <td align="center">node 17.3</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/reactjs_logo.png?raw=true" alt="ReactJS" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/reactjs_name.png?raw=true" alt="ReactJS" height="50" /></td>
            <td align="center">16.14.0</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/redux_logo.png?raw=true" alt="Redux" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/redux_name.png?raw=trueg" alt="Redux" height="50" /></td>
            <td align="center">4.1.1</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/bootstrap_logo.png?raw=true" alt="Bootstrap" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/bootstrap_name.png?raw=true" alt="Bootstrap" height="50" /></td>
            <td align="center">5.1.3</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/ckeditor_logo.png?raw=true" alt="CKEditor" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/ckeditor_name.png?raw=true" alt="CKEditor" height="50" /></td>
            <td align="center">5</td>
        </tr>
    </tbody>
</table>

## Install & Use with Docker
[Before starting, you can learn how to configure the server →](https://github.com/kosyachniy/dev/blob/master/server/SERVER.md)

### Local
1. Customize file ` docker/.env `

2. Run
```
make run
```

3. Open ` http://localhost/ `

### Production
1. Customize file ` docker/.env `

2. Run Docker Compose
```
make deploy
```

3. Open ` https://web.kosyachniy.com/ ` (your link)

### Production (with metrics)
Here you need to complete step 10 from [SERVER.md](https://github.com/kosyachniy/dev/blob/master/server/SERVER.md)

1. Customize files ` docker/.env ` & ` docker/docker-compose.metrics.yml `

2. Run to configure MongoDB (if not done)
```
make deploy
```
And stop it

3. Run cluster
```
make node
```

4. Open ` https://web.kosyachniy.com/ ` (your link)
