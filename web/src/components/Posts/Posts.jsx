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
		const { online, t } = this.props

		return (
			<div className="album py-5 bg-light">
				<div className="container">
					{ online.count && (
						<div className="row">
								<div style={ {width: '100%'} }>
									{t('system.online')}: { online.count}
								</div>
								<div style={ {width: '100%'} }>
									{ online.users.map((user) => (
										<div className="badge badge-secondary" key={ user.id }>
											{ user.id }
										</div>
									))}
								</div>
						</div>
					)}
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