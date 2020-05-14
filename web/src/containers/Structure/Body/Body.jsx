import React from 'react'
import { Route, Switch } from 'react-router-dom'

import { socketIO } from '../../../func/sockets'

import './style.css'

// System
import Loader from '../../../components/Loader'

// Users
import Profile from '../../Pages/Profile'

// Posts
import PostsGrid from '../../Posts/Grid'
import PostsFeed from '../../Posts/Feed'
import PostsPost from '../../Posts/Post'
import PostsEdit from '../../Posts/Edit'

// Map
import Map from '../../Pages/Map'


export default class App extends React.Component {
	componentWillMount() {
		const token = localStorage.getItem('token')

		// Online

		socketIO.on('connect', () => {
			socketIO.emit('online', {token})
		})

		socketIO.on('online_add', (x) => {
			// console.log('ADD', x)
			this.props.onlineAdd(x)
		})

		socketIO.on('online_del', (x) => {
			// console.log('DEL', x)
			this.props.onlineDelete(x)
		})

		socketIO.on('disconnect', () => {
			this.props.onlineReset();
		})
	}

	render() {
		if (this.props.online.count && !this.props.system.loaded) {
			this.props.systemLoaded();
		}

		return (
			<>
				<Loader
					loaded={this.props.system.loaded}
					theme={this.props.system.theme}
					color={this.props.system.color}
				/>
				<div className={`bg-${this.props.system.theme}`}>
					<div className="container" id="main">
						<Switch>
							<Route exact path="/">
								<PostsGrid />
							</Route>

							<Route path="/posts">
								<PostsGrid />
							</Route>
							<Route path="/post/add">
								<PostsEdit />
							</Route>
							<Route path="/post">
								<PostsPost />
							</Route>
							<Route path="/feed">
								<PostsFeed />
							</Route>

							<Route path="/profile">
								<Profile />
							</Route>

							<Route path="/map">
								<Map />
							</Route>
						</Switch>
					</div>
				</div>
			</>
		)
	}
}