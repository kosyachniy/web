import openSocket from 'socket.io-client';

export default openSocket(process.env.NEXT_PUBLIC_WEB, {
  transports: ['websocket'],
  upgrade: false,
});
