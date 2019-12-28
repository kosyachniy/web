import React from 'react'

import api from '../../func/api'

import Post from './Post'


export default class Main extends React.Component {
	state = {
		posts: [],
	}

	getPost = (data={}) => {
		const handlerSuccess = (res) => {
			this.setState({
				posts: res['posts'],
			})
		}

		api('posts.get', data, handlerSuccess)
	}

	componentWillMount() {
		this.getPost()
	}

	render() {
		return (
			<div className="album py-5 bg-light">
				<div className="container">
					<div className="row">
						{ this.state.posts.map((el, num) =>
							<Post el={ el } key={ num } />
						) }
					</div>
				</div>
			</div>
		)
	}
}