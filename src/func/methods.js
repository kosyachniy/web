import api from './api'


function getPost(that) {
	const handlerSuccess = (other, res) => {
		other.setState({cont: res['post']['cont']})
	}

	api('post', 'get', that, handlerSuccess)
}


export default getPost