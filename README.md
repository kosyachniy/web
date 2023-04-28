# Template full stack application
[![.github/workflows/deploy.yml](https://github.com/kosyachniy/web/actions/workflows/deploy.yml/badge.svg)](https://github.com/kosyachniy/web/actions/workflows/deploy.yml)

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
            <td rowspan="5" align="center">DevOps</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/docker_logo.png?raw=true" alt="Docker" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/docker_name.png?raw=true" alt="Docker" height="50" /></td>
            <td align="center">20.10.21</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/nginx_logo.png?raw=true" alt="NGINX" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/nginx_name.png?raw=true" alt="NGINX" height="50" /></td>
            <td align="center">1.23</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/letsencrypt_logo.png?raw=true" alt="Let's Encrypt" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/letsencrypt_name.png?raw=true" alt="Let's Encrypt" height="50" /></td>
            <td align="center"></td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/grafana_logo.png?raw=true" alt="Grafana" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/grafana_name.png?raw=true" alt="Grafana" height="50" /></td>
            <td align="center">9.2.5</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/prometheus_logo.png?raw=true" alt="Prometheus" height="50" /></td>
            <td></td>
            <td align="center">2.40.1</td>
        </tr>
        <tr>
            <td rowspan="5" align="center">Back-end</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/python_logo.png?raw=true" alt="Python" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/python_name.png?raw=true" alt="Python" height="50" /></td>
            <td align="center">3.10</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/fastapi_logo.png?raw=true" alt="FastAPI" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/fastapi_name.png?raw=true" alt="FastAPI" height="50" /></td>
            <td align="center">0.87</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/mongodb_logo.png?raw=true" alt="MongoDB" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/mongodb_name.png?raw=true" alt="MongoDB" height="50" /></td>
            <td align="center">6.0</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/redis_logo.png?raw=true" alt="Redis" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/redis_name.png?raw=true" alt="Redis" height="50" /></td>
            <td align="center">7.0</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/socketio_logo.png?raw=true" alt="Socket.IO" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/socketio_name.png?raw=true" alt="Socket.IO" height="50" /></td>
            <td align="center"></td>
        </tr>
        <tr>
            <td rowspan="6" align="center">Front-end</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/javascript_logo.png?raw=true" alt="JavaScript" height="50" /></td>
            <td></td>
            <td align="center">node 19.1</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/reactjs_logo.png?raw=true" alt="ReactJS" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/reactjs_name.png?raw=true" alt="ReactJS" height="50" /></td>
            <td align="center">18.2</td>
        </tr>
        <tr>
            <td></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/nextjs_name.png?raw=true" alt="Next.js" height="50" /></td>
            <td align="center">13.0.3</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/redux_logo.png?raw=true" alt="Redux" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/redux_name.png?raw=trueg" alt="Redux" height="50" /></td>
            <td align="center">4.2</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/bootstrap_logo.png?raw=true" alt="Bootstrap" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/bootstrap_name.png?raw=true" alt="Bootstrap" height="50" /></td>
            <td align="center">5.2.1</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/ckeditor_logo.png?raw=true" alt="CKEditor" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/ckeditor_name.png?raw=true" alt="CKEditor" height="50" /></td>
            <td align="center">5</td>
        </tr>
    </tbody>
</table>

## Run
[Before starting, you can learn how to configure the server →](https://github.com/kosyachniy/dev/blob/main/server/SERVER.md)

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
                1. Configure <code> .env </code> from <code> base.env </code> and add:
                <pre>
# Type
# LOCAL / TEST / DEV / PRE / PROD
MODE=LOCAL<br />

\# Links
PROTOCOL=http
EXTERNAL_HOST=localhost
EXTERNAL_PORT=80
DATA_PATH=./data
                </pre>
            </td>
            <td valign="top">
                1. Configure <code> .env </code> from <code> base.env </code> and add:
                <pre>
\# Type
\# LOCAL / TEST / DEV / PRE / PROD
MODE=PROD

\# Links
PROTOCOL=https
EXTERNAL_HOST=web.kosyachniy.com
WEB_PORT=8201
API_PORT=8202
JOBS_PORT=8203
TG_PORT=8204
DB_PORT=8205
REDIS_PORT=8206
PROMETHEUS_PORT=8207
GRAFANA_PORT=8208
DATA_PATH=~/web/data # or change to global path, for example: ~/data/web
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
