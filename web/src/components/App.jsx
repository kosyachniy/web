import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.css'

import i18n from './i18n'

import Header from './Structure/Header'
import Body from './Structure/Body'
import Footer from './Structure/Footer'


export default class App extends React.Component {
	handlerLang = (lang) => {
		localStorage.setItem('lang', lang)
		i18n.changeLanguage(lang)
	}

	render() {
		return (
			<BrowserRouter>
				<Header />

				<Body />

				<Footer handlerLang={ this.handlerLang } />
			</BrowserRouter>
		)
	}
}