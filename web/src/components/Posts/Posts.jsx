import React from 'react'
import openSocket from 'socket.io-client'

import api from '../../func/api'

import './style.css'
import Post from './Post'

import { socket } from '../../sets'


export default class Main extends React.Component {
	getPost = (data={}) => {
		const handlerSuccess = (res) => {
			this.props.postsGet(res['posts']);
		}

		api('posts.get', data, handlerSuccess)
	}

	componentWillMount() {
		// Online

		// const socketIO = openSocket(`${socket.link}main`)

		// Posts

		this.getPost()
	}

	render() {
		const { online } = this.props
		console.log(online)

		return (
			<div className="album py-5 bg-light">
				<div className="container">
					{ online.count && (
						<div className="row">
								<div style={ {width: '100%'} }>
									Онлайн: { online.count}
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