import React from 'react'
import ReactHtmlParser from 'react-html-parser'

import { getPost } from '../../func/methods'


export default class Post extends React.Component {
	constructor(props) {
		super(props)

		this.state = {
			posts: [],
		}
	}

	// post: {
	// 	cover: 0,
	// 	name: 'Title',
	// 	description: 'Description',
	// },

	// state = {
	// 	posts: [],
	// }

	componentWillMount() {
		// if(this.props.user.id === undefined || (this.props.user.id !== undefined && this.props.user.id === 0)) {
		// 	this.props.onRedirect('/ladders')
		// }

		let postID = Number(document.location.pathname.split('/').pop())
		getPost(this, {id: postID})
	}

	render() {
		return (
			<div className="col-md-4">
				<div className="card mb-4 shadow-sm">
					{ this.state.posts.map((post, num) =>
						<React.Fragment>
							<img src={ post.cover } alt={ post.name } />
							<p>{ post.name }</p>
						</React.Fragment>
					)}
				</div>
			</div>
		)
	}
}