import React from 'react'
import { Link } from 'react-router-dom'
import { withTranslation } from 'react-i18next'

import api from '../../../func/api'

import './style.css'


class Feed extends React.Component {
	getPost = (data={}) => {
		const handlerSuccess = (res) => {
			this.props.postsGet(res['posts']);
		}

		api('posts.get', data, handlerSuccess)
	}

	componentWillMount() {
		this.getPost()
	}

	getTime = (time) => {
		const newTime = new Date(time * 1000);

		const year = newTime.getFullYear();
		let day = `${newTime.getDate()}`;
		let hours = `${newTime.getHours()}`;
		let minutes = `${newTime.getUTCMinutes()}`;

		let month = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'][newTime.getMonth()];

		if (day.length < 2) {
			day = `0${day}`
		}

		if (hours.length < 2) {
			hours = `0${hours}`
		}

		if (minutes.length < 2) {
			minutes = `0${minutes}`
		}

		return `${day} ${month} ${year} в ${hours}:${minutes}`;
	}

	render() {
		const { t } = this.props

		return (
			<>
				<div className="container" id="feed">
					<Link to="/post/add">
						<button
							type="button"
							className="btn btn-success"
							style={ {width: '100%'} }
						>
							<i className="fas fa-plus" />
						</button>
					</Link>

					{ !this.props.posts.length && (
						<p>{ t('posts.empty') }!</p>
					) }

					{ this.props.posts.map(post => (
						<div className="cards" key={ post.id }>
							<div className="time">{ this.getTime(post.time) }</div>
							<div className="additional"><i className="fas fa-ellipsis-v" /></div>
							<Link to={ `/post/${post.id}` } >
								<h3 className="title">{ post.name }</h3>
								{ post.cover && (
									<img src={ post.cover } alt={ post.name } />
								) }
								<div className="content short">{ post.cont }</div>
							</Link>
							<div className="reactions">
								<div><i className="fas fa-share" />{ post.reactions.reposts ? " " + post.reactions.reposts : "" }</div>
								<div><i className="far fa-heart" />{ post.reactions.likes ? " " + post.reactions.likes : "" }</div>
								{/* <i className="fas fa-heart" /> */}
								<div><i className="far fa-comment" /> { post.reactions.comments.length ? " " + post.reactions.comments.length : "" }</div>
							</div>
						</div>
					)) }
				</div>
			</>
		)
	}
}

export default withTranslation()(Feed);