import api from './api'


// Posts

export function getPost(that, data={}) {
	const handlerSuccess = (other, res) => {
		let posts = res['result']

		// if (posts.length == 1) {
		// 	other.setState({
		// 		post: posts['articles'][0],
		// 	})
		// } else {

		other.setState({
			posts: posts['articles'],
		})

		// }
	}

	api(that, 'articles.get', data, handlerSuccess)
}

export function updatePost(that, data) {
	data = {'cont': data}

	api(that, 'articles.edit', data)
}