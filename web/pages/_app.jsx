import Head from 'next/head'
import { useRouter } from 'next/router'
import { appWithTranslation } from 'next-i18next'
import { Provider } from 'react-redux'
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
import makeStore from '../redux/store'
import { systemPrepared, systemLoaded, systemLoadedLocale } from '../redux/actions/system'
import { changeLang, setUtm } from '../redux/actions/main'
import { onlineAdd, onlineDelete, onlineReset } from '../redux/actions/online'
import { categoriesGet } from '../redux/actions/categories'
import api from '../lib/api'
import socketIO from '../lib/sockets'
// import Loader from '../components/Loader'

// Structure
import Header from '../components/Header'
import Footer from '../components/Footer'

// Users
import Auth from '../components/Auth'
import AuthMail from '../components/Auth/Mail'
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
    const system = useSelector(state => state.system)
    const main = useSelector(state => state.main)
    const online = useSelector(state => state.online)
    const categories = useSelector(state => state.categories)

    useEffect(() => {
        // Online
        socketIO.emit('online', { token: main.token })
        socketIO.on('online_add', x => dispatch(onlineAdd(x)))
        socketIO.on('online_del', x => dispatch(onlineDelete(x)))
        socketIO.on('disconnect', () => dispatch(onlineReset()))
    }, [])

    useEffect(() => {
        // UTM
        if (router.isReady) {
            if (router.query['utm'] && !main.utm) {
                dispatch(setUtm(router.query['utm']))
            }
            dispatch(systemPrepared())
        }
    }, [router.query])

    useEffect(() => {
        if (system.prepared && (categories === null || main.locale !== system.loaded_locale)) {
            api(main, 'categories.get', {locale: main.locale}).then(res => {
                dispatch(categoriesGet(res.categories))
                dispatch(systemLoadedLocale(main.locale))
            })
        }
    }, [system.prepared, categories, main.locale])

    useEffect(() => {
        if (system.loaded_locale === null) {
            dispatch(systemLoadedLocale(main.locale))
        }
    }, [main.locale])

    useEffect(() => {
        // Locale
        if (main.locale !== router.locale) {
            dispatch(changeLang(router.locale))
        }

        // Loaded
        if (online.count && !system.loaded) {
            dispatch(systemLoaded())
        }
    })

    return (
        <>
            {/* <Loader /> */}

            <div className={ `bg-${main.theme}` }>
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

const { store, persistor } = makeStore()

const App = pageProps => (
    <Provider store={store}>
        <PersistGate persistor={persistor}>
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


export default appWithTranslation(App)
