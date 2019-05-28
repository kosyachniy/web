import api from './api'


// Articles

export function getPost(that, data={}) {
	const handlerSuccess = (other, res) => {
		other.setState({
			posts: res['result']['articles'],
		})
	}

	const handlerError = (other, res) => {
		console.log(res)
	}

	api(that, 'articles.get', data, handlerSuccess, handlerError)
}