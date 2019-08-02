import React from 'react'
import ReactHtmlParser from 'react-html-parser'

import { getPost } from '../../func/methods'

import Editor from './Editor'


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
			<div className="bg-light">
				{ this.state.posts.map((post, num) =>
					<React.Fragment>
						<React.Fragment key={ num }>
							<h1>{ post.name }</h1>
							<img src={ post.cover } alt={ post.name } />
							{ ReactHtmlParser(post.cont) }
						</React.Fragment>
					
						<Editor id={ post.id } cont={ post.cont }/>
					</React.Fragment>
				)}
			</div>
		)
	}
}