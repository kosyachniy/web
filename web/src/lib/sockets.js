import openSocket from 'socket.io-client'


export const socketIO = openSocket(process.env.REACT_APP_WEB, {
    transports: ['websocket'],
    upgrade: false,
})
