"""Base connection for AMQP communications.

This file contains the base class for create a communications with a AMQP
connection. It also is able to run the connections on a separate loop in separate
thread to not interfere with the current loop and thread.
"""

from __future__ import annotations

import asyncio
from asyncio import AbstractEventLoop, CancelledError
from threading import Thread
from typing import NoReturn, Union, Optional
from urllib.parse import urlparse, ParseResult

import aio_pika
from aio_pika import Connection, Channel, Exchange
from loguru import logger

from .credentials import EdgeCredentials


class BasePubSub:
    """BasePubSub is used as a Base class for RabbitMQ connections"""

    def __init__(self,
                 url: Optional[Union[str, ParseResult]] = None,
                 *,
                 host: str = 'localhost', port: int = 30133,
                 credentials: Optional[EdgeCredentials] = None,
                 username: str, password: str = 'Password01!',
                 exchange_name: str,
                 loop: Optional[AbstractEventLoop] = None):
        """
        :param url: if present, used this to initialize connection.
        :param host: if url not present, use this host to connect.
        :param port: if url not present, use this port to connect.
        :param credentials: if url not present, use these credentials to connect.
        :param username: if url and credential not present, use this username to connect.
        :param password: if url and credential not present, use this password to connect.
        :param exchange_name: Name of the exchange to connect.
        :param loop: Loop used to execute async functions.
        """

        if url is not None:
            if isinstance(url, str):
                url = urlparse(url)
            host = url.hostname
            port = url.port
            username = url.username
            password = url.password

        if credentials is None:
            credentials = EdgeCredentials(username, password)

        self._host = host
        self._port = port
        self._credentials = credentials

        self._exchange_name = exchange_name

        self._connection: Optional[Connection] = None
        self._channel: Optional[Channel] = None
        self._exchange: Optional[Exchange] = None

        self._loop = loop if loop is not None else asyncio.get_event_loop()

        self._thread: Optional[Thread] = None

    @property
    def host(self) -> str:
        """Host of the connection."""

        return self._host

    @property
    def port(self) -> int:
        """Port of the connection."""

        return self._port

    @property
    def credentials(self) -> EdgeCredentials:
        """Credential used to identify and sign in."""

        return EdgeCredentials(self._credentials.username, self._credentials.password)

    @property
    def url(self) -> str:
        """URL used for the connection."""

        return f"amqp://{self._credentials.username}:{self._credentials.password}@{self._host}:{self._port}"

    @property
    def url_no_password(self) -> str:
        """URL used for the connection."""

        return f"amqp://{self._credentials.username}:{'*' * len(self._credentials.password)}@{self._host}:{self._port}"

    @property
    def loop(self) -> AbstractEventLoop:
        """Loop used to run async func."""

        return self._loop

    async def __aenter__(self):
        return await self.connect()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.close()

    def loop_in_other_thread(self) -> bool:
        """Check if the connection is running in different thread from the one who call this method.

        :return: True if the connection is in other thread and loop and False in other case.
        """

        return self._loop is not None and self._loop != asyncio.get_event_loop()

    async def _connect(self, loop=None):
        self._connection: Connection = await aio_pika.connect(host=self._host, port=self._port,
                                                              login=self._credentials.username,
                                                              password=self._credentials.password,
                                                              loop=loop, timeout=10)
        logger.debug("Connected to {}", self._connection.url)
        self._connection.close_callbacks.add(self._on_connection_close)
        self._channel: Channel = await self._connection.channel()
        logger.debug("Channel %d to {} created", self._channel.number, self._connection.url)
        self._exchange: Exchange = await self._channel.get_exchange(self._exchange_name)
        logger.debug("Got exchange {} from channel %d from {}",
                     self._exchange.name, self._channel.number, self._connection.url)

        return self

    async def connect(self) -> BasePubSub:
        """Connect to RabbitMQ

        :return: self
        """

        if self.loop_in_other_thread():  # Check if connect must be done in other Thread and loop.
            logger.info("Connecting to {} on thread {}", self.url, self._thread.name)
            return asyncio.run_coroutine_threadsafe(self._connect(self._loop), self._loop).result()
        logger.info("Connecting to {}", self.url)
        return await self._connect(self._loop)

    def _run(self) -> NoReturn:
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_forever()
        finally:
            logger.debug("Thread closed")
            self._loop.close()
            self._thread = None

    def run(self) -> BasePubSub:
        """Create a Thread to execute all the communications.

        :return: self
        """

        if self.loop_in_other_thread():
            logger.error("Thread id already running")
            raise RuntimeError("Thread id already running")
        self._loop = asyncio.new_event_loop()
        self._thread = Thread(target=self._run)
        self._thread.start()

        logger.debug("{} running on thread", self.__class__.__name__)

        return self

    async def _close(self) -> NoReturn:
        await self._channel.close()
        await self._connection.close()

        self._exchange = None
        self._channel = None
        self._connection = None

    async def close(self) -> NoReturn:
        """Close the connection to RabbitMQ and stop thread if necessary."""

        logger.info("Closing connection to {}", self.url)
        if self.loop_in_other_thread():
            asyncio.run_coroutine_threadsafe(self._close(), self._loop).result()
            asyncio.run_coroutine_threadsafe(self._loop.shutdown_asyncgens(), self._loop).result()
            self._loop.call_soon_threadsafe(self._loop.stop)
            if self._thread is not None and self._thread.is_alive():
                self._thread.join()
            self._loop = None
            self._thread = None
        else:
            await self._close()

    def is_closed(self) -> bool:
        """Check if the connection is closed

        :return: True if the connection is closed and False in other cases.
        """

        return self._connection.is_closed if self._connection is not None else True

    def _on_connection_close(self, connection: Connection, exception: BaseException) -> NoReturn:
        """Call this function when connection close.

        :param connection: The closing connection.
        :param exception: If present, the exception that cause the close.
        """

        if exception and not isinstance(exception, CancelledError):
            logger.info("Connection to {} closed due to {}", connection.url, exception)
        else:
            logger.info("Connection to {} closed", connection.url)
        self._exchange = None
        self._channel = None
        self._connection = None
