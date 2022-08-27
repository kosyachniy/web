import { useState, useEffect } from 'react'
import { BrowserRouter } from 'react-router-dom'

// Redux
import { Provider } from 'react-redux';
import { store } from '../redus';

// import styles from '../styles/base.module.css'

// Structure
import Header from '../containers/Structure/Header'
import Body from '../containers/Structure/Body'
import Footer from '../containers/Structure/Footer'

// Users
import Auth from '../containers/Pages/Auth'
import Mail from '../containers/Pages/Mail'
import Online from '../containers/Pages/Online'


export default () => {
    const [showPopUp, setShowPopUp] = useState(false)

    // useEffect(() => {
    // }, [])

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
