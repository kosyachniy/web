import React from 'react'
import { Route, Switch } from 'react-router-dom'

import Posts from '../../Posts'
import Post from '../../Post'


export default function Body() {
	return (
			<div className="container" id="main">
				<Switch>
					<Route exact path="/posts">
						<Posts />
					</Route>

					<Route path="/post">
						<Post />
					</Route>
				</Switch>
			</div>
	)
}