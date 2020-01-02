import React from 'react'
import openSocket from 'socket.io-client'

import api from '../../func/api'

import './style.css'
import Post from './Post'

import { socket } from '../../sets'


export default class Main extends React.Component {
	state = {
		online: {count: null, users: []},
	}

	getPost = (data={}) => {
		const handlerSuccess = (res) => {
			this.props.postsGet(res['posts']);
		}

		api('posts.get', data, handlerSuccess)
	}

	componentWillMount() {
		// Online

		const socketIO = openSocket(`${socket.link}main`)

		socketIO.on('online_add', (x) => {
			console.log('ADD', x)
			this.setState({
				count: x['count'],
				online: x['users'],
			})
		})

		socketIO.on('online_del', (x) => {
			console.log('DEL', x)
			this.setState({
				count: x['count'],
				online: x['users'],
			})
		})

		// Posts

		this.getPost()
	}

	render() {
		return (
			<div className="album py-5 bg-light">
				<div className="container">
					{ this.state.count && (
						<div className="row">
								<div style={ {width: '100%'} }>
									Онлайн: { this.state.count}
								</div>
								<div style={ {width: '100%'} }>
									{ this.state.online.map((user) => (
										<div className="badge badge-secondary" key={ user.sid }>
											{ user.sid }
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