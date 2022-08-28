import { useState, useEffect } from 'react'
import Head from 'next/head'
import { Provider, useSelector, useDispatch } from 'react-redux'
import { persistStore } from 'redux-persist'
import { PersistGate } from 'redux-persist/integration/react'

import {
    useStore,
    systemLoaded,
    onlineAdd, onlineDelete, onlineReset,
} from '../store'
// import '../styles/main.css'
import '../styles/header.css'
import '../styles/body.css'
// import styles from '../styles/base.module.css'

import { socketIO } from '../functions/sockets'

// System
import Loader from '../components/Loader'

// Structure
import Header from '../containers/Structure/Header'
// import Body from '../containers/Structure/Body'
import Footer from '../containers/Structure/Footer'

// // Users
// import Auth from '../containers/Pages/Auth'
// import Mail from '../containers/Pages/Mail'
// import Online from '../containers/Pages/Online'


const Body = ({ Component, pageProps }) => {
    const dispatch = useDispatch()
    const system = useSelector((state) => state.system)
    const online = useSelector((state) => state.online)

    useEffect(() => { // WillMount
        // Online

        socketIO.on('connect', () => {
            socketIO.emit('online', {token})
        })

        socketIO.on('online_add', (x) => {
            // console.log('ADD', x)
            dispatch(onlineAdd(x))
        })

        socketIO.on('online_del', (x) => {
            // console.log('DEL', x)
            dispatch(onlineDelete(x))
        })

        socketIO.on('disconnect', () => {
            dispatch(onlineReset())
        })
    }, [])

    useEffect(() => {
        if (online.count && !system.loaded) {
            dispatch(systemLoaded())
        }
    })

    return (
        <>
            { system.token }

            <Loader />

            <div className={`bg-${system.theme}`}>
                <div className="container" id="main">
                    <Component { ...pageProps } />
                </div>
            </div>
        </>
    )
}


export default (pageProps) => {
    const store = useStore(pageProps.initialReduxState)
    const persistor = persistStore(store, {}, function () {
      persistor.persist()
    })

    const [showPopUp, setShowPopUp] = useState(false)

    return (
        <Provider store={store}>
            <PersistGate loading={<div>loading</div>} persistor={persistor}>
                <Head>
                    <title>{ process.env.NEXT_PUBLIC_NAME }</title>
                    {/* Zoom */}
                    <meta
                        name="viewport"
                        content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"
                    />
                </Head>
                <Header handlerPopUp={ setShowPopUp } />

                <Body { ...pageProps } />

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
            </PersistGate>
        </Provider>
    )
}
