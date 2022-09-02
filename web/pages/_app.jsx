import Head from 'next/head'
import { Provider } from 'react-redux'
import { persistStore } from 'redux-persist'
import { PersistGate } from 'redux-persist/integration/react'
import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'

// import '../styles/main.css'
import '../styles/header.css'
import '../styles/body.css'
// import styles from '../styles/base.module.css'
import {
    useStore,
    systemLoaded, onlineAdd, onlineDelete, onlineReset,
} from '../store'
import { socketIO } from '../../functions/sockets'
import Loader from '../../components/Loader'

// Structure
import Header from '../components/Header'
import Footer from '../components/Footer'

// Users
import Auth from '../components/Auth'
import AuthMail from '../components/AuthMail'
import Online from '../components/Online'


const Body = ({ Component, pageProps }) => {
    const dispatch = useDispatch()
    const system = useSelector((state) => state.system)
    const online = useSelector((state) => state.online)

    useEffect(() => {
        // Online

        socketIO.on('connect', () => {
            socketIO.emit('online', {token: system.token})
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
            <Loader />

            <div className={`bg-${system.theme}`}>
                <div className="container" id="main">
                    <Component { ...pageProps } />
                </div>
            </div>

            { system.popup === 'auth' && (
                <Auth />
            ) }
            { system.popup === 'mail' && (
                <AuthMail />
            ) }
            { system.popup === 'online' && (
                <Online />
            ) }
        </>
    )
}

export default (pageProps) => {
    const store = useStore(pageProps.initialReduxState)
    const persistor = persistStore(store, {}, function () {
      persistor.persist()
    })

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
                <Header />
                <Body { ...pageProps } />
                <Footer />
            </PersistGate>
        </Provider>
    )
}
