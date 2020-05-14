# Template full stack application
## Description
Form | Side | Stack | Language | Path
---|---|---|---|---
API | Back-end | Flask | Python | ``` api/ ```
Web app | Front-end | React | JavaScript | ``` web/ ```
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
			<td rowspan="2">Back-end</td>
			<td><img src="re/img/flask_logo.png" alt="Flask" height="70" /></td>
			<td><img src="re/img/flask_name.png" alt="Flask" height="70" /></td>
		</tr>
		<tr>
			<td><img src="re/img/mongodb_logo.png" alt="MongoDB" height="70" /></td>
			<td><img src="re/img/mongodb_name.png" alt="MongoDB" height="70" /></td>
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
1. Customize files ``` api/keys.json ``` & ``` web/src/keys.js ``` & ``` docker/.env ```

2. Run Docker Compose
```
cd docker/
docker-compose up --build
```

3. Open
Go to ``` http://localhost/ ```

## Install
### Back-end
1. Change folder
```
cd api/
```

2. Customize files ``` sets.py ``` & ``` keys.json ```

3. Virtual environment
```
python3 -m venv env
env/bin/pip install -r requirements.txt
```

### Front-end
1. Change folder
```
cd web/
```

2. Customize files ``` src/sets.js ``` & ``` src/keys.js ```

3. Virtual environment
```
npm install
```

OR

```
npm run build
```

## Usage
### Back-end
```
env/bin/gunicorn app:app -k eventlet -w 1 -b :5000 --reload
```

### Front-end
```
npm start
```

OR

```
serve -s build -p 3000
```