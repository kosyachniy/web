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

## Start
### Back-end
1. Customize files ``` sets.py ``` & ``` keys.py ```

2. Virtual environment
```
python3 -m venv env
env/bin/pip install -r requirements.txt
```

3. Run
```
env/bin/gunicorn app:app -c run.py
```

### Front-end
1. Virtual environment
```
npm install
```

2. Run
```
npm start
```