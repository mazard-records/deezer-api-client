import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from queue import Queue
from threading import Thread
from typing import Any, Optional
from urllib.parse import urlencode, urlparse

import httpx

from ._const import DEFAULT_CONNECT_URL


class DeezerAuthServer(Thread):
    """ A background server that generates Deezer access token. """

    def __init__(
        self,
        access_token_url: str,
        access_token_receiver: Queue,
    ) -> None:
        super().__init__()
        self._access_token_url = access_token_url
        self._access_token_receiver = access_token_receiver
        self._server: Optional[HTTPServer] = None

    def shutdown(self) -> None:
        if self._server is None:
            raise IOError("Server is not started")
        self._server.shutdown()

    def run(self, *args: Any, **kwargs: Any) -> None:
        this = self
        class DeezerRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                query = urlparse(self.path).query
                components = dict(
                    component.split("=")
                    for component in query.split("&")
                )
                code = components.get("code")
                response = httpx.get(f"{this._access_token_url}&code={code}")
                response.raise_for_status()
                result = response.json()
                token = result.get("access_token")
                this._access_token_receiver.put(token)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                # TODO: send auto close page.
                self.end_headers()

        self._server = HTTPServer(("localhost", 8080), DeezerRequestHandler)
        self._server.serve_forever()


def DeezerAccessToken(
    application_id: str,
    secret_id: str,
    scopes: list[str],
) -> str:
    args = urlencode(
        dict(
            app_id=application_id,
            secret=secret_id,
            output="json",
        )
    )
    access_token_url = f"{DEFAULT_CONNECT_URL}/access_token.php?{args}"
    access_token_receiver = Queue(maxsize=-1)
    server = DeezerAuthServer(access_token_url, access_token_receiver)
    server.start()
    args = urlencode(
        dict(
            app_id=application_id,
            redirect_uri="http://localhost:8080/redirect",
            perms=",".join(scopes),
        )
    )
    webbrowser.open(f"{DEFAULT_CONNECT_URL}/auth.php?{args}")
    access_token = access_token_receiver.get(block=True, timeout=None)
    server.shutdown()
    server.join()
    return access_token
