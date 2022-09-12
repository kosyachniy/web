import Head from 'next/head'
import { useRouter } from 'next/router'
import { appWithTranslation } from 'next-i18next'
import { Provider } from 'react-redux'
import { persistStore } from 'redux-persist'
import { PersistGate } from 'redux-persist/integration/react'
import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
    faEnvelope,
    faGenderless,
    faPlus,
    faShare,
    faPencil,
    faTrash,
    faEllipsisVertical,
    faSun,
    faMoon,
    faTableCellsLarge,
    faListUl,
} from '@fortawesome/free-solid-svg-icons'
import {
    faHeart,
    faComment,
    faEye,
    faFloppyDisk,
    faImage,
} from '@fortawesome/free-regular-svg-icons'
import {
    faVk,
    faGoogle,
    faTelegram,
} from '@fortawesome/free-brands-svg-icons'

import '../styles/main.css'
import styles from '../styles/body.module.css'
import {
    useStore,
    systemLoaded, onlineAdd, onlineDelete, onlineReset,
    changeLang,
} from '../store'
import { socketIO } from '../functions/sockets'
import Loader from '../components/Loader'

// Structure
import Header from '../components/Header'
import Footer from '../components/Footer'

// Users
import Auth from '../components/Auth'
import AuthMail from '../components/AuthMail'
import Online from '../components/Online'


library.add(
    faEnvelope,
    faGenderless,
    faPlus,
    faHeart,
    faComment,
    faShare,
    faEye,
    faPencil,
    faTrash,
    faEllipsisVertical,
    faSun,
    faMoon,
    faFloppyDisk,
    faTableCellsLarge,
    faListUl,
    faImage,
    faVk,
    faGoogle,
    faTelegram,
)


const Body = ({ Component, pageProps }) => {
    const router = useRouter()
    const dispatch = useDispatch()
    const system = useSelector((state) => state.system)
    const online = useSelector((state) => state.online)

    useEffect(() => {
        // Locale
        dispatch(changeLang(router.locale))

        // Online

        // socketIO.on('online', () => {
        socketIO.emit('online', { token: system.token })
        // })

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
        // Loaded
        if (online.count && !system.loaded) {
            dispatch(systemLoaded())
        }
    })

    return (
        <>
            {/* <Loader /> */}

            <div className={ `bg-${system.theme}` }>
                <div className={ `container ${styles.main}` }>
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

const App = (pageProps) => {
    const store = useStore(pageProps.initialReduxState)
    const persistor = persistStore(store, {}, () => { persistor.persist() })

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


export default appWithTranslation(App)
