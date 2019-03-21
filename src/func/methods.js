import api from './api'


function getPost(that) {
	const req = {
		'method': 'post.get',
	}

	const handlerSuccess = (other, res) => {
		other.setState({cont: res['cont']})
	}

	api(that, req, handlerSuccess)
}


export default getPost