from flask import render_template, request
from app import app

from requests import post
from json import loads


@app.route('/', methods=['GET'])
@app.route('/index')
@app.route('/index/')
def index():
	req = {
		'method': 'system.test',
		'ip': request.remote_addr,
	}
	res = loads(post(request.url, json=req).text)

	return render_template('index.html',
		cont = res,
	)