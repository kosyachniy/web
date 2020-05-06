import React from 'react'
import { Link } from 'react-router-dom'
import { withTranslation } from 'react-i18next'

import api from '../../../func/api'

import Card from '../../../components/Card'


class Grid extends React.Component {
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
			<>
				<div className="album py-4">
					<Link to="/post/add">
						<button
							type="button"
							className="btn btn-success"
							style={ {width: '100%'} }
						>
							<i className="fas fa-plus" />
						</button>
					</Link>
				</div>

				<div className="album py-2">
					<div className="row">
						{ this.props.posts.map((el, num) =>
							<Card post={ el } key={ num } />
						) }
					</div>
				</div>
			</>
		)
	}
}

export default withTranslation()(Grid);