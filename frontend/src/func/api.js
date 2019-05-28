import axios from 'axios'


function serverRequest(adr, method='get', json={}) {
	const link = 'http://0.0.0.0:5000/' + adr + '/'

	if (method === 'get') {
		return axios.get(link)
	} else if (method === 'post') {
		return axios.post(link, json)
	} else if (method === 'put') {
		return axios.put(link, json)
	} else if (method === 'delete') {
		return axios.delete(link)
	}
}

function handlerResult(that, res, handlerSuccess) {
	if (res['error']) {
		console.log(res)
	} else {
		handlerSuccess(that, res)
	}
}

export default function api(adr, method, that, req={}, handlerSuccess=()=>{}) {
	req['language'] = 'ru'

	serverRequest(adr, method, req).then((res) => handlerResult(that, res.data, handlerSuccess))
}