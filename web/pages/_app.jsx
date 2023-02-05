import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Head from 'next/head'
import { useRouter } from 'next/router'
import { appWithTranslation } from 'next-i18next'

import '../styles/main.css'
import styles from '../styles/body.module.css'
import wrapper from '../redux/store'
import { systemPrepared } from '../redux/actions/system'
import { changeLang, setUtm } from '../redux/actions/main'
import { onlineAdd, onlineDelete, onlineReset } from '../redux/actions/online'
import { categoriesGet, categoriesClear } from '../redux/actions/categories'
import api from '../lib/api'
import socketIO from '../lib/sockets'

import Header from '../components/Structure/Header'
import Footer from '../components/Structure/Footer'
import Auth from '../components/Auth'
import AuthMail from '../components/Auth/Mail'
import Online from '../components/Online'
import Toasts from '../components/Toast'


const App = ({ Component, pageProps }) => {
    const router = useRouter()
    const dispatch = useDispatch()
    const system = useSelector(state => state.system)
    const main = useSelector(state => state.main)
    const online = useSelector(state => state.online)
    const categories = useSelector(state => state.categories)

    // Online
    useEffect(() => {
        if (system.prepared && !online.count) {
            socketIO.emit('online', { token: main.token })
            socketIO.on('online_add', x => dispatch(onlineAdd(x)))
            socketIO.on('online_del', x => dispatch(onlineDelete(x)))
            socketIO.on('disconnect', () => dispatch(onlineReset()))
        }
    }, [router.asPath, system.prepared])

    // UTM
    useEffect(() => {
        if (router.isReady) {
            router.query['utm'] && !main.utm && dispatch(setUtm(router.query['utm']))
            dispatch(systemPrepared())
        }
    }, [router.query])

    useEffect(() => {
        dispatch(categoriesClear())
    }, [main.locale])

    useEffect(() => {
        system.prepared && categories === null && api(main, 'categories.get', {locale: main.locale}).then(
            res => dispatch(categoriesGet(res.categories))
        )
    }, [system.prepared, categories])

    useEffect(() => {
        dispatch(changeLang(router.locale))
    }, [router.locale])

    return (
        <>
            <Head>
                <title>{ process.env.NEXT_PUBLIC_NAME }</title>
                {/* Zoom */}
                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"
                />
            </Head>

            <Header />

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

            <Toasts toasts={ system.toasts } />

            <Footer />
        </>
    )
}


export default wrapper.withRedux(appWithTranslation(App))
