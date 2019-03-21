import axios from 'axios'


function serverRequest(adr, method, json) {
	const link = 'http://0.0.0.0:5000/' + adr + '/'

	if (method === 'get') {
		return axios.get(link)
	} else if (method === 'post') {
		return axios.post(link)
	}
}

function handlerResult(that, res, handlerSuccess) {
	if (res['error']) {
		that.setState({cont: res['message']})
	} else {
		handlerSuccess(that, res)
	}
}

export default function api(adr, method, that, handlerSuccess, req={}) {
	req['language'] = 'ru'

	serverRequest(adr, method, req).then((res) => handlerResult(that, res.data, handlerSuccess))
}