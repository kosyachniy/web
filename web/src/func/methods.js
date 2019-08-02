import api from './api'


// Posts

export function getPost(that, data={}) {
	const handlerSuccess = (other, res) => {
		let posts = res['result']['posts']

		// if (posts.length == 1) {
		// 	other.setState({
		// 		post: posts[0],
		// 	})
		// } else {

		other.setState({
			posts: posts,
		})

		// }
	}

	api(that, 'posts.get', data, handlerSuccess)
}

export function updatePost(that, data) {
	api(that, 'posts.edit', data)
}