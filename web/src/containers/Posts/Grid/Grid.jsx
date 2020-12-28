import { useEffect } from 'react';
import { Link } from 'react-router-dom'
import { withTranslation } from 'react-i18next'

import api from '../../../func/api'

import Card from '../../../components/Card'


const Grid = (props) => {
	// const { t } = props

	const getPost = (data={}) => {
		const handlerSuccess = (res) => {
			props.postsGet(res['posts']);
		}

		api('posts.get', data, handlerSuccess)
	}

	useEffect(() => {
		getPost()
	}, [])

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
					{ props.posts.map((el, num) =>
						<Card post={ el } key={ num } />
					) }
				</div>
			</div>
		</>
	)
}

export default withTranslation()(Grid);