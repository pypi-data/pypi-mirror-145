from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send


class MetricsRedirect:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("path"):
            if scope["path"] == "/metrics":
                scope["path"] = "/metrics/"
                scope["raw_path"] = b"/metrics/"
        await self.app(scope, receive, send)
