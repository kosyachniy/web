import React from 'react'
import { BrowserRouter } from 'react-router-dom'

// Redux
import { Provider } from 'react-redux';
import { store } from './redus';

// Structure
import Header from './containers/Structure/Header'
import Body from './containers/Structure/Body'
import Footer from './containers/Structure/Footer'

// Users
import Auth from './containers/Pages/Auth'
import Mail from './containers/Pages/Mail'
import Online from './containers/Pages/Online'


function genereteToken() {
    const res = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    return res.substr(0, 32);
}


export default class App extends React.Component {
	state = {
		showPopUp: false,
	}

	handlerPopUp = (page) => {
		this.setState({ showPopUp: page })
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
		const { showPopUp } = this.state;

		return (
			<Provider store={store}>
				<BrowserRouter>
					<Header handlerPopUp={ this.handlerPopUp } />

					<Body />

					{ showPopUp && (
						<>
							{ showPopUp === 'auth' && (
								<Auth handlerPopUp={ this.handlerPopUp } />
							) }
							{ showPopUp === 'mail' && (
								<Mail handlerPopUp={ this.handlerPopUp } />
							) }
							{ showPopUp === 'online' && (
								<Online handlerPopUp={ this.handlerPopUp } />
							) }
						</>
					) }

					<Footer />
				</BrowserRouter>
			</Provider>
		)
	}
}