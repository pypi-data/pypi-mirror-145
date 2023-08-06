"""Asyncronous Python client for DiematicServer"""
import aiohttp
import async_timeout
import asyncio
from socket import gaierror as SocketGIAError
import logging

from .enums import (
    DiematicOperation,
)

from .__version__ import __version__
from yarl import URL
from .models import Boiler
from deepmerge import always_merger
from typing import Any, Optional

from .exceptions import (
    DiematicConnectionError,
    DiematicParseError,
    DiematicResponseError,
)
import json

_LOGGER = logging.getLogger(__name__)


class DiematicBoilerClient:
    """Main class for handling connections with Diematic HTTP servers."""

    def __init__(
        self,
        host: str,
        port: int = 8080,
        base_path: str = "/diematic/",
        request_timeout: int = 8,
        session: aiohttp.client.ClientSession = None,
        tls: bool = False,
        username: str = None,
        password: str = None,
        verify_ssl: bool = False,
        user_agent: str = None,
    ) -> None:
        """Initialize connection with Diematic server."""
        self._session = session
        self._close_session = False

        self.base_path = base_path
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.request_timeout = request_timeout
        self.tls = tls
        self.verify_ssl = verify_ssl
        self.user_agent = user_agent

        self.diematic_uri = self._build_diematic_uri()

        if user_agent is None:
            self.user_agent = f"PythonDiematicClient{__version__}"

    def _build_diematic_uri(self):
        """Build a valid URI to connect to service"""
        scheme = "https" if self.tls else "http"

        return URL.build(
            scheme=scheme, host=self.host, port=self.port, path=self.base_path
        ).human_repr()

    def _message(self, operation: DiematicOperation, msg: dict) -> dict:
        """Build a request message to be sent to the server."""
        base = {"operation": operation}

        if msg is not dict:
            msg = {}
        if operation == DiematicOperation.GET_CONFIG:
            msg["uri"] = "config"
        elif operation == DiematicOperation.GET_VALUES:
            msg["uri"] = "json"

        return always_merger.merge(base, msg)

    async def _request(
        self,
        uri: str = "",
        data: Optional[Any] = None,
        params: Optional[dict] = None,
    ) -> dict:
        """Handle a request to a Diematic server."""
        scheme = "https" if self.tls else "http"

        method = "GET"
        url = URL.build(
            scheme=scheme, host=self.host, port=self.port, path=self.base_path
        ).join(URL(uri))

        auth = None
        if self.username and self.password:
            auth = aiohttp.BasicAuth(self.username, self.password)

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/plain, */*",
            "Connection": "keep-alive",
            "Keep-Alive": "timeout=5, max=100",
            "Cache-Control": "max-age=0",
        }

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    method,
                    url,
                    auth=auth,
                    data=data,
                    params=params,
                    headers=headers,
                    ssl=self.verify_ssl,
                )
                try:
                    if (response.status // 100) in [4, 5]:
                        content = response.read()

                        raise DiematicResponseError(
                            f"HTTP {response.status}",
                            {
                                "content-type": response.headers.get("Content-type"),
                                "message": content.decode("utf-8"),
                                "status-code": response.status,
                            },
                        )

                    if "content-length" in response.headers.keys():
                        length = response.headers["content-length"]
                        content = await response.content.readexactly(int(length))
                        return json.loads(content)

                    return await response.json()

                finally:
                    response.close()

        except asyncio.TimeoutError as exc:
            raise DiematicConnectionError(
                "Timeout occurred while connecting to Diematic server."
            ) from exc
        except (aiohttp.ClientError, SocketGIAError) as exc:
            raise DiematicConnectionError(
                "Error occurred while communicating with Diematic server."
            ) from exc
        finally:
            if self._close_session:
                await self._session.close()
                self._session = None

    async def execute(self, operation: DiematicOperation, message: dict) -> dict:
        """Send a request message to the server."""
        message = self._message(operation, message)
        return await self._request(data=message, uri=message["uri"])

    async def boiler(self) -> Boiler:
        """Get boiler information from server."""
        response_data = await self.execute(DiematicOperation.GET_VALUES, {})

        try:
            boiler = Boiler.from_dict(response_data)
        except Exception as exc:
            raise DiematicParseError from exc

        return boiler

    async def config(self) -> list:
        """Bet Boiler registers configuration from server."""
        response_data = await self.execute(DiematicOperation.GET_CONFIG, {})

        return response_data
