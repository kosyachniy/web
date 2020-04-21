# Full stack application
## Description
Form | Side | Stack | Language | Path
---|---|---|---|---
API | Back-end | Flask | Python | ``` api/ ```
Web app | Front-end | React | JavaScript | ``` web/ ```
iOS | Front-end | React Native | JavaScript | planned
Android | Front-end | React Native | JavaScript | planned

### Stack
#### DevOps
<img src="re/img/docker.png" alt="Docker" height="100" /> &nbsp; <img src="re/img/nginx.png" alt="NGINX" height="100" />

#### Back-end
<img src="re/img/flask.png" alt="Flask" height="100" /> &nbsp; <img src="re/img/mongodb.png" alt="MongoDB" height="100" />

#### Front-end
<img src="re/img/reactjs.png" alt="ReactJS" height="100" /> &nbsp; <img src="re/img/redux.png" alt="Redux" height="100" /> &nbsp; <img src="re/img/bootstrap.png" alt="Bootstrap 4" height="100" /> &nbsp; <img src="re/img/ckeditor.png" alt="CKEditor 5" height="100" />

## Install & Use with Docker
1. Customize files ``` sets.py ``` & ``` keys.json ``` & ``` src/sets.js ``` & ``` src/keys.js ```

2. Run Docker Compose
```
cd docker/
docker-compose up --build
```

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