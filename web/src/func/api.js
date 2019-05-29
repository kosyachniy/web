import axios from 'axios'
import { server } from '../sets'

function serverRequest(json={}) {
	return axios.post(server.link, json)
}

function handlerResult(that, res, handlerSuccess, handlerError) {
	if (res['error']) {
		console.log(res)
		handlerError(that, res)
	} else {
		// console.log(res)
		handlerSuccess(that, res)
	}
}

export default function api(that, method, params={}, handlerSuccess=()=>{}, handlerError=()=>{}) {
	let json = {
		'method': method,
		'params': params,
	}

	json['language'] = localStorage.getItem('lang')
	json['token'] = JSON.parse(localStorage.getItem('user')).token

	serverRequest(json).then((res) => handlerResult(that, res.data, handlerSuccess, handlerError))
}