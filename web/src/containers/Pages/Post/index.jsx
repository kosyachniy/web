import React from 'react'
// import ReactHtmlParser from 'react-html-parser'
import MathJax from 'react-mathjax-preview'

import api from '../../../func/api'

import './style.css'
import Edit from '../PostEdit'


class Post extends React.Component {
	constructor(props) {
		super(props)

		this.state = {
			post: null,
			edit: false,
		}
	}

	getPost = (data={}) => {
		const handlerSuccess = (res) => {
			this.setState({
				post: res['posts'][0],
			})
		}

		api('posts.get', data, handlerSuccess)
	}

	savePost = () => {
		this.getPost({ id: this.state.post.id })
		this.setState({ edit: false })
	}

	componentWillMount() {
		let postID = Number(document.location.pathname.split('/').pop())
		this.getPost({id: postID})
	}

	render() {
		const { post } = this.state

		if (post) {
			if (this.state.edit) {
				return (
					<Edit
						post={ post }
						handlerSave={ this.savePost }
					/>
				)
			} else {
				return (
					<>
						<div className="album py-2">
							<h1>{ post.name }</h1>

							<button
								className="btn btn-outline-secondary"
								onClick={ () => {this.setState({ edit: true })} }
							>
								<i className="far fa-edit" />
							</button>

							{/* <img src={ post.cover } alt={ post.name } /> */}

							<br /><br />
							<MathJax math={ post.cont } />
						</div>
					</>
				)
			}
		} else {
			return (<>123</>)
		}
	}
}

export default Post;