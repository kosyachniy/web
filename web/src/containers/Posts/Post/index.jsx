import React from 'react'
import { Redirect } from 'react-router-dom'
// import ReactHtmlParser from 'react-html-parser'
import MathJax from 'react-mathjax-preview'

import api from '../../../func/api'

import './style.css'
import Edit from '../Edit'
import Map from '../../../components/Map'


class Post extends React.Component {
	constructor(props) {
		super(props)

		this.state = {
			post: null,
			edit: false,
			deleted: false,
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

	deletePost = () => {
		const data = {
			id: this.state.post.id,
		}

		const handlerSuccess = (res) => {
			this.setState({ deleted: true })
		}

		api('posts.delete', data, handlerSuccess)
	}

	componentWillMount() {
		let postID = Number(document.location.pathname.split('/').pop())
		this.getPost({id: postID})
	}

	render() {
		const { post } = this.state

		if (this.state.deleted) {
			return (
				<Redirect to="/" />
			)
		}

		if (post) {
			return (
				<div id="post">
					<div className="album py-2">
						<h1>{ post.name }</h1>

						{ this.state.edit && (
							<button
								className="btn btn-outline-secondary"
								onClick={ () => {this.setState({ edit: false })} }
							>
								<i className="far fa-eye" />
							</button>
						) || (
							<button
								className="btn btn-outline-secondary"
								onClick={ () => {this.setState({ edit: true })} }
							>
								<i className="far fa-edit" />
							</button>
						) }
						<button
							className="btn btn-danger"
							onClick={ this.deletePost }
						>
							<i className="far fa-trash-alt" />
						</button>

						{ this.state.edit && (
							<Edit
								post={ post }
								handlerSave={ this.savePost }
							/>
						) || (
							<>
								{/* <img src={ post.cover } alt={ post.name } /> */}
								<br /><br />
								<MathJax math={ post.cont } />

								<div style={{ marginTop: '50px', height: '250px' }}>
									{ post.geo && (
										<Map center={ post.geo} zoom={ 14 } />
									) || (
										<Map />
									)}

								</div>
							</>
						) }
					</div>
				</div>
			)
		} else {
			return (<></>)
		}
	}
}

export default Post;