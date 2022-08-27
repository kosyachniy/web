import Head from 'next/head'

import '../styles/main.css'


export default ({ Component, pageProps }) => {
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
            <Component {...pageProps} />
        </>
    )
}
