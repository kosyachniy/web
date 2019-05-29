import api from './api'


// Posts

export function getPost(that, data={}) {
	const handlerSuccess = (other, res) => {
		other.setState({
			posts: res['result']['articles'],
		})
	}

	api(that, 'articles.get', data, handlerSuccess)
}

export function updatePost(that, data) {
	data = {'cont': data}

	api(that, 'articles.edit', data)
}