import jwt
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from lib import log


class AccessMiddleware(BaseHTTPMiddleware):
    """Access checking middleware"""

    def __init__(self, app, jwt_secret, whitelist):
        super().__init__(app)
        self.jwt = jwt_secret
        self.whitelist = whitelist

    async def dispatch(self, request: Request, call_next):
        url = request.url.path[4:]

        # TODO: check current ip with token ip

        token = request.cookies.get("Authorization") or request.headers.get(
            "Authorization"
        )

        # Whitelist
        if request.method != "POST" or (not token and url in self.whitelist):
            request.state.token = None
            request.state.user = 0
            request.state.network = 0
            return await call_next(request)

        if not token:
            # log.warning("No token\n{}", {
            #     'url': url,
            # })
            return Response(content="Invalid token", status_code=401)

        # JWT
        if " " in token:
            token = token.split(" ")[1]
        if not token or token == "null":
            log.warning(
                "Invalid token\n{}",
                {
                    "url": url,
                    "token": token,
                },
            )
            return Response(content="Invalid token", status_code=401)

        try:
            token = jwt.decode(token, self.jwt, algorithms="HS256")
        except Exception as e:  # pylint: disable=broad-except
            log.warning(
                "Invalid token\n{}",
                {
                    "url": url,
                    "token": token,
                    "error": e,
                },
            )
            return Response(content="Invalid token", status_code=401)

        request.state.token = token["token"]
        request.state.user = token["user"]
        request.state.network = token["network"]

        return await call_next(request)
