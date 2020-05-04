import React from 'react'
// import ReactHtmlParser from 'react-html-parser'
import MathJax from 'react-mathjax-preview'
import { withTranslation } from 'react-i18next'

import api from '../../../func/api'

import './style.css'
import Editor from '../../../components/Editor'


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

	updatePost = (cont) => {
		this.setState({ post: {...this.state.post, cont} })
	}

	savePost = () => {
		const handlerSuccess = (res) => {
			if (res.cont) {
				this.setState({ post: {...this.state.post, cont: res.cont} })
			}
		}

		api('posts.edit', this.state.post, handlerSuccess)
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

						<Editor
							id={ post.id }
							cont={ post.cont }
							updatePost={ this.updatePost }
						/>

						<br />
						<input
							type="button"
							className="btn btn-success"
							style={ {width: '100%'} }
							value={ t('system.save') }
							onClick={ this.savePost }
						/>
					</>
				) }
			</div>
		)
	}
}

export default withTranslation()(Post);