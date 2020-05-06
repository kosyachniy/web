import React from 'react'
// import ReactHtmlParser from 'react-html-parser'
import MathJax from 'react-mathjax-preview'
import { withTranslation } from 'react-i18next'

import api from '../../../func/api'

import './style.css'


class Post extends React.Component {
	constructor(props) {
		super(props)

		this.state = {
			post: null,
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

	componentWillMount() {
		let postID = Number(document.location.pathname.split('/').pop())
		this.getPost({id: postID})
	}

	render() {
		const { post } = this.state;
		const { t } = this.props

		return (
			<div>
				{ post && (
					<>
						<h1>{ post.name }</h1>
						<img src={ post.cover } alt={ post.name } />

						<MathJax math={ post.cont } />
					</>
				) }
			</div>
		)
	}
}

export default withTranslation()(Post);