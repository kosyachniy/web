import { useState, useEffect } from 'react'
// import { useDispatch } from 'react-redux'
import { useSelector } from 'react-redux'

// import styles from '../styles/base.module.css'

// Structure
import Header from '../containers/Structure/Header'
// import Body from '../containers/Structure/Body'
import Footer from '../containers/Structure/Footer'

// // Users
// import Auth from '../containers/Pages/Auth'
// import Mail from '../containers/Pages/Mail'
// import Online from '../containers/Pages/Online'


export default ({ Component, pageProps }) => {
    const [showPopUp, setShowPopUp] = useState(false)
    // const dispatch = useDispatch()
    const token = useSelector((state) => state.token)

    // useEffect(() => {
    // }, [])

    return (
        <>
            <Header handlerPopUp={ setShowPopUp } />
            {/* <Component { ...pageProps } /> */}

            {token}

            {/* { showPopUp && (
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
            ) } */}

            <Footer />
        </>
    )
}
