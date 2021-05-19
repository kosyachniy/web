// Socket.IO
import openSocket from 'socket.io-client'
import { sockets } from '../sets'


export const socketIO = openSocket(sockets, {
    transports: ['websocket'],
    upgrade: false,
})