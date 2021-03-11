// Socket.IO
import openSocket from 'socket.io-client'
import { socket } from '../sets'


export const socketIO = openSocket(`${socket.link}`, { transports: ['websocket'], upgrade: false })