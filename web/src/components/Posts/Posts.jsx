import React from 'react'
import { withTranslation } from 'react-i18next'

import api from '../../func/api'

import './style.css'
import Post from './Post'


class Posts extends React.Component {
	getPost = (data={}) => {
		const handlerSuccess = (res) => {
			this.props.postsGet(res['posts']);
		}

		api('posts.get', data, handlerSuccess)
	}

	componentWillMount() {
		this.getPost()
	}

	render() {
		// const { t } = this.props

		return (
			<div className="album py-5 bg-light">
				<div className="container">
					<div className="row">
						{ this.props.posts.map((el, num) =>
							<Post el={ el } key={ num } />
						) }
					</div>
				</div>
			</div>
		)
	}
}

export default withTranslation()(Posts);