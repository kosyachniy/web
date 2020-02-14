# Full stack application
## Description
Essence | Side | Stack | Language | Path
---|---|---|---|---
API | Back-end | Flask | Python | ``` api/ ```
Web app | Front-end | React | JavaScript | ``` web/ ```
iOS | Front-end | React Native | JavaScript | planned
Android | Front-end | React Native | JavaScript | planned

### Stack
<img src="re/img/flask.png" height="100" />
<img src="re/img/reactjs.png" height="100" />
<img src="re/img/mongodb.png" height="100" />
<img src="re/img/bootstrap.png" height="100" />
<img src="re/img/ckeditor.png" height="100" />

## Installation
### Back-end
1. Change folder
```
cd api/
```

2. Customize files ``` sets.py ``` & ``` keys.py ```

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
cd api/
env/bin/gunicorn app:app -c run.py
```

### Front-end
```
cd web/
npm start
```

OR

```
cd web/
serve -s build -p 3000
```