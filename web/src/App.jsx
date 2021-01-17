import React, { useState, useEffect } from 'react'
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


const App = () => {
	const [showPopUp, setShowPopUp] = useState(false)

	useEffect(() => { // WillMount
		// Token

		let token = localStorage.getItem('token')

		if (token === null) {
			token = genereteToken()
			localStorage.setItem('token', token)
		}
	}, [])

	return (
		<Provider store={store}>
			<BrowserRouter>
				<Header handlerPopUp={ setShowPopUp } />

				<Body />

				{ showPopUp && (
					<>
						{ showPopUp === 'auth' && (
							<Auth handlerPopUp={ setShowPopUp } />
						) }
						{ showPopUp === 'mail' && (
							<Mail handlerPopUp={ setShowPopUp } />
						) }
						{ showPopUp === 'online' && (
							<Online handlerPopUp={ setShowPopUp } />
						) }
					</>
				) }

				<Footer />
			</BrowserRouter>
		</Provider>
	)
}

export default App;