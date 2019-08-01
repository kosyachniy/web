import React from 'react'
import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.css'

import Header from './Structure/Header'
import Body from './Structure/Body'
import Footer from './Structure/Footer'


export default class App extends React.Component {
	render() {
		return (
			<React.Fragment>
				<Header />

				<Body />

				<Footer />
			</React.Fragment>
		)
	}
}