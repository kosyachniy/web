import axios from 'axios'
import { server } from '../sets'

function serverRequest(json={}) {
	return axios.post(server.link, json)
}

function handlerResult(res, handlerSuccess, handlerError) {
	if (res['error']) {
		console.log(res)
		handlerError(res)
	} else {
		console.log(res)
		handlerSuccess(res['result'])
	}
}

export default function api(method, params={}, handlerSuccess=()=>{}, handlerError=()=>{}) {
	let json = {
		'method': method,
		'params': params,
	}

	json['language'] = localStorage.getItem('lang')
	json['token'] = localStorage.getItem('token')

	console.log(json)

	serverRequest(json).then((res) => handlerResult(res.data, handlerSuccess, handlerError))
}