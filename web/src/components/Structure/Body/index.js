import React from 'react'
import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom'

import Posts from '../../Posts/Main'
import Post from '../../Post/Main'


export default function Body() {
	return (
		<BrowserRouter>
			<div className="container" id="main">
				<Switch>
					<Route exact path="/">
						<Posts />
					</Route>

					<Route path="/post">
						<Post />
					</Route>
				</Switch>
			</div>
		</BrowserRouter>
	)
}