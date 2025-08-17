import socketio


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
asgi = socketio.ASGIApp(sio)


__all__ = (
    "sio",
    "asgi",
)
