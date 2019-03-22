import api from './api'


function getPost(that) {
	const handlerSuccess = (other, res) => {
		other.setState({cont: res['post']['cont']})
	}

	api('post', 'get', that, {}, handlerSuccess)
}

function updatePost(that, data) {
	const req = {
		'cont': data,
	}

	api('post', 'put', that, req)
}

export { getPost, updatePost }