// Socket.IO
import openSocket from 'socket.io-client'
import { socket } from '../sets'


export const socketIO = openSocket(`${socket.link}main`, { transports: ['websocket'], upgrade: false })