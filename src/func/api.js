function serverRequest(json) {
	return new Promise(function(resolve, reject) {
		const request = require("request");
		request({
			'url': 'http://0.0.0.0:5000/',
			'method': 'POST',
			'json': json,
		}, function(error, response, body) {
			if (!error && response.statusCode === 200) {
				resolve(body)
			} else {
				console.log("error: " + error)
			}
		})
	})
}

function handlerResult(that, res, handlerSuccess) {
	if (res['error']) {
		that.setState({cont: res['message']})
	} else {
		handlerSuccess(that, res)
	}
}

export default function api(that, req, handlerSuccess) {
	req['language'] = 'ru'

	serverRequest(req).then((res) => handlerResult(that, res, handlerSuccess))
}