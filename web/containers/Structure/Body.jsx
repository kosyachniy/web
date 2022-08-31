import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'

import { systemLoaded, onlineAdd, onlineDelete, onlineReset } from '../../store'
import { socketIO } from '../../functions/sockets'
import Loader from '../../components/Loader'

// // Users
// import Auth from '../containers/Pages/Auth'
// import Mail from '../containers/Pages/Mail'
// import Online from '../containers/Pages/Online'


export default ({ Component, pageProps }) => {
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
        </>
    )
}
