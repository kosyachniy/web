import React from 'react'
import { Link } from 'react-router-dom'

import { getPost } from '../../func/methods'

import Post from './Post'
import Editor from './Editor'


export default class Main extends React.Component {
	state = {
		posts: [],
	}

	componentWillMount() {
		getPost(this)
	}

	render() {
		return (
			<div className="album py-5 bg-light">
				<div className="container">
					<div className="row">
						{ this.state.posts.map((el, num) =>
							<Link to={ '/post/' } key={ num }>
								<Post key={ num } el={ el } />
							</Link>
						) }
						<Editor />
					</div>
				</div>
			</div>
		)
	}
}