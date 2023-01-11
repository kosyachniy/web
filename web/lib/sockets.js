import openSocket from 'socket.io-client'


export const socketIO = openSocket(process.env.NEXT_PUBLIC_WEB, {
    transports: ['websocket'],
    upgrade: false,
})
