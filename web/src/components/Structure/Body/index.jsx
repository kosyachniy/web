import React from 'react'
import { Route, Switch } from 'react-router-dom'

import Posts from '../../Posts'
import Post from '../../Post'

import './style.css'


export default function Body() {
	return (
		<div className="container" id="main">
			<Switch>
				<Route exact path="/">
					<Posts />
				</Route>

				<Route path="/posts">
					<Posts />
				</Route>

				<Route path="/post">
					<Post />
				</Route>
			</Switch>
		</div>
	)
}