import Head from 'next/head'
import { Provider } from 'react-redux'
import { persistStore } from 'redux-persist'
import { PersistGate } from 'redux-persist/integration/react'

// import '../styles/main.css'
import '../styles/header.css'
import '../styles/body.css'
// import styles from '../styles/base.module.css'
import { useStore } from '../store'

// Structure
import Header from '../containers/Structure/Header'
import Body from '../containers/Structure/Body'
import Footer from '../containers/Structure/Footer'


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
