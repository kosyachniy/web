import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.css'
import i18n from './i18n'

// Redux
import { Provider } from 'react-redux';
import { store } from './redus';

import Header from './Structure/Header'
import Body from './Structure/Body'
import Footer from './Structure/Footer'
import Auth from './Auth'


function genereteToken() {
    const res = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    return res.substr(0, 32);
}


export default class App extends React.Component {
	state = {
		showAuth: false,
	}

	handlerLang = (lang) => {
		localStorage.setItem('lang', lang)
		i18n.changeLanguage(lang)
	}

	handlerLogIn = (status) => {
		this.setState({ showAuth: status })
	}

	componentWillMount() {
		// Token

		let token = localStorage.getItem('token')

		if (token === null) {
			token = genereteToken()
			localStorage.setItem('token', token)
		}
	}

	render() {
		const { showAuth } = this.state;

		return (
			<Provider store={store}>
				<BrowserRouter>
					<Header
						handlerLang={ this.handlerLang }
						handlerLogIn={ this.handlerLogIn }
					/>

					<Body />

					{ showAuth && (
						<Auth handlerLogIn={ this.handlerLogIn } />
					) }

					<Footer handlerLang={ this.handlerLang } />
				</BrowserRouter>
			</Provider>
		)
	}
}