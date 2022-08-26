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
            <td align="center">1.21.6</td>
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
            <td align="center">3.10</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/fastapi_logo.png?raw=true" alt="FastAPI" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/fastapi_name.png?raw=true" alt="FastAPI" height="50" /></td>
            <td align="center">0.75.0</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/mongodb_logo.png?raw=true" alt="MongoDB" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/master/media/logos/png/mongodb_name.png?raw=true" alt="MongoDB" height="50" /></td>
            <td align="center">5.0.6</td>
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
            <td align="center">node 16.14.0</td>
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

## Run
[Before starting, you can learn how to configure the server →](https://github.com/kosyachniy/dev/blob/master/server/SERVER.md)

<table>
    <thead>
        <tr>
            <th>local</th>
            <th>prod</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td valign="top">
                1. Configure ` .env `
                <pre>
# Type
# LOCAL / TEST / DEV / PRE / PROD
MODE=LOCAL

\# Links
PROTOCOL=http
EXTERNAL_HOST=localhost
EXTERNAL_PORT=80
                </pre>
            </td>
            <td valign="top">
                1. Configure ` .env `
                <pre>
\# Type
\# LOCAL / TEST / DEV / PRE / PROD
MODE=PROD

\# Links
PROTOCOL=https
EXTERNAL_HOST=web.kosyachniy.com
WEB_PORT=8201
API_PORT=8202
TG_PORT=8203
                </pre>
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <pre>
\# NOTE: The names HOST, PORT, MAIL are reserved

\# Base info
NAME=Web app
PROJECT_NAME=web

\# Contacts
EMAIL=
PHONE=
SOCIAL="[{\"title\": \"vk\", \"data\": \"https://vk.com/alexeypoloz\"}, {\"title\": \"fb\", \"data\": \"https://www.facebook.com/alexeypoloz\"}, {\"title\": \"in\", \"data\": \"https://www.linkedin.com/in/alexeypoloz/\"}, {\"title\": \"ig\", \"data\": \"https://instagram.com/mr.poloz/\"}]"

\# Data
PATH_TO_DATA=./data
SIDE_OPTIMIZED=250

\# Default
LOCALE=ru
TIMEZONE=3

\# Payments
SUBSCRIPTION_DAY=
SUBSCRIPTION_WEEK=
SUBSCRIPTION_MONTH=
SUBSCRIPTION_SEASON=
SUBSCRIPTION_ACADEMIC_YEAR=
SUBSCRIPTION_YEAR=

\# Inner
DISCOUNT=1

\# Grafana
GRAFANA_PASS=

\# MongoDB
MONGO_USER=
MONGO_PASS=

\# Redis
REDIS_HOST=redis
REDIS_PASS=

\# YooKassa
YOOKASSA_ID=
YOOKASSA_SECRET=

\# Google
GOOGLE_ID=
GOOGLE_SECRET=

\# Telegram
TG_TOKEN=
TG_BOT=
BUG_CHAT=

\# VK
VK_ID=
VK_SECRET=

\# SMSC
SMSC_USER=
SMSC_PASS=

\# Google Maps
GOOGLE_MAPS_KEY=
GOOGLE_MAPS_LAT=59.9392
GOOGLE_MAPS_LNG=30.3165
GOOGLE_MAPS_ZOOM=12

\# Google Docs
GOOGLE_DOCS_ID=
GOOGLE_DOCS_SECRET=
GOOGLE_DOCS_TYPE=service_account
GOOGLE_DOCS_PROJECT=
GOOGLE_DOCS_EMAIL=
GOOGLE_DOCS_CLIENT=
GOOGLE_DOCS_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_DOCS_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_DOCS_AUTH_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_DOCS_CLIENT_CERT_URL=
GOOGLE_SHEET=

\# Agora
AGORA_APP_ID=
AGORA_CUSTOMER_ID=
AGORA_CUSTOMER_CERTIFICATE=

\# Amazon
AMAZON_ID=
AMAZON_SECRET=
AMAZON_BUCKET=
AMAZON_DIR=local
AMAZON_REGION=

\# Redis
REDIS_HOST=redis
REDIS_PASS=
                </pre>
            </td>
        </tr>
        <tr>
            <td>
                2. <code> make dev </code>
            </td>
            <td>
                2. <code> make run </code>
            </td>
        </tr>
        <tr>
            <td>
                3. Open ` http://localhost/ `
            </td>
            <td>
                3. Open ` https://web.kosyachniy.com/ ` (your link)
            </td>
        </tr>
    </tbody>
</table>


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
