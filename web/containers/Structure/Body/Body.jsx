import React, { useEffect } from 'react'
import { Route, Routes } from 'react-router-dom'

import { getToken } from '../../../lib/token'
import { socketIO } from '../../../lib/sockets'

import './style.css'

// System
import Loader from '../../../components/Loader'
import Callback from '../../Pages/Callback'

// Users
import Profile from '../../Pages/Profile'

// Posts
import PostsGrid from '../../Posts/Grid'
import PostsFeed from '../../Posts/Feed'
import PostsPost from '../../Posts/Post'
import PostsEdit from '../../Posts/Edit'

// // Map
// import Map from '../../Pages/Map'


const App = (props) => {
    useEffect(() => { // WillMount
        let token = getToken()

        // Online

        socketIO.on('connect', () => {
            socketIO.emit('online', {token})
        })

        socketIO.on('online_add', (x) => {
            // console.log('ADD', x)
            props.onlineAdd(x)
        })

        socketIO.on('online_del', (x) => {
            // console.log('DEL', x)
            props.onlineDelete(x)
        })

        socketIO.on('disconnect', () => {
            props.onlineReset()
        })
    }, [])

    useEffect(() => { // Fix for "Cannot update a component (`ConnectFunction`) while rendering a different component (`App`). To locate the bad setState() call inside `App`, follow the stack trace as described in https://fb.me/setstate-in-render"
        if (props.online.count && !props.system.loaded) {
            props.systemLoaded()
        }
    })

    return (
        <>
            <Loader
                loaded={props.system.loaded}
                theme={props.system.theme}
                color={props.system.color}
            />
            <div className={`bg-${props.system.theme}`}>
                <div className="container" id="main">
                    <Routes>
                        <Route exact path="/" element={<PostsGrid />} />

                        <Route path="/posts" element={<PostsGrid />} />
                        <Route path="/post/add" element={<PostsEdit />} />
                        <Route path="/post" element={<PostsPost />} />
                        <Route path="/feed" element={<PostsFeed />} />

                        <Route path="/profile" element={<Profile />} />

                        {/* <Route path="/map" element={<Map />} /> */}

						<Route path="/callback" element={<Callback />} />
                    </Routes>
                </div>
            </div>
        </>
    )
}

export default App;
