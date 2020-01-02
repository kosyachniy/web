import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.css'
import openSocket from 'socket.io-client'

import i18n from './i18n'

import Header from './Structure/Header'
import Body from './Structure/Body'
import Footer from './Structure/Footer'

import { socket } from '../sets'


function genereteToken() {
    const res = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    return res.substr(0, 32);
}


export default class App extends React.Component {
	handlerLang = (lang) => {
		localStorage.setItem('lang', lang)
		i18n.changeLanguage(lang)
	}

	componentWillMount() {
		// Token

		let token = localStorage.getItem('token')

		if (token === null) {
			token = genereteToken()
			localStorage.setItem('token', token)
		}

		// Online

		const socketIO = openSocket(`${socket.link}main`)

		socketIO.on('connect', () => {
			socketIO.emit('online', {token})
		})
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