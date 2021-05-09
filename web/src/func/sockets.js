// Socket.IO
import openSocket from 'socket.io-client'
import { sockets } from '../sets'


export const socketIO = openSocket(`${sockets}`, {
	cors: {
		origin: "*",
		methods: ["GET", "POST"],
		transports: ['websocket', 'polling'],
		credentials: true,
	},
	allowEIO3: true,
	// transports: ['websocket'],
	// upgrade: false,
})