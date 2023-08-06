"""Altair Smartworks Edge Compute Platform driver wrapper.

This script contains all the driver calls for the Altair Smartworks Edge
Compute Platform using async calls that increase performance. This allows
to receive property updates, action requests and Thing updates.
"""

from __future__ import annotations

import asyncio
import json
import time
from typing import NoReturn, Any, Union, Optional, Callable, Coroutine
from urllib.parse import ParseResult

from aio_pika.abc import AbstractIncomingMessage, AbstractQueue
from loguru import logger

from .base_pubsub import BasePubSub
from .credentials import EdgeCredentials


class Driver(BasePubSub):
    """Altair Smartworks Edge Compute Platform driver wrapper.

    Driver connect to Edge Compute Platform to allow you to interact
    with SmartWorks IoT ECP driver exchange. Can run in background to allow calls for
    others thread without mutual block. It allows receiving property updates,
    action requests and Thing updates.
    """

    def __init__(self, url: Optional[Union[str, ParseResult]] = None,
                 *,
                 credentials: Optional[EdgeCredentials] = None,
                 username: str = 'device-driver-user',
                 driver_exchange_name: str = 'ase.exchange.driver',
                 queue_prefix: str = 'ase.queue.driver',
                 **kwargs):
        """
        :param url: if present, used this to initialize connection to RabbitMQ server.
        :param credentials: if url not present, use these credentials to connect to RabbitMQ server.
        :param username: if url and credential not present, use this username to connect to RabbitMQ server.
        :param driver_exchange_name: Name of the driver exchange to connect to RabbitMQ server.
        :param queue_prefix: Name of the queue prefix for receiving updates and request.
        """

        super().__init__(url, credentials=credentials, username=username, exchange_name=driver_exchange_name, **kwargs)

        self._queue_prefix = queue_prefix
        self._subscribed_things = {}

    async def _close(self):
        task = [self.unsubscribe(thing_id) for thing_id in self._subscribed_things]
        await asyncio.gather(*task)

        await super()._close()

    async def subscribe(self,
                        thing_id: str,
                        *,
                        on_set_property: Optional[Callable[[str, Any], Coroutine[NoReturn]]] = None,
                        on_request_action: Optional[Callable[[str, str, ...], Coroutine[NoReturn]]] = None,
                        on_update: Optional[Callable[[dict[str, Any]], Coroutine[NoReturn]]] = None) -> str:
        """Subscribe the Thing ID for receive updates.

        Subscribe the Thing ID for receive updates depending on the callback functions.
        At least one function callback if necessary.
        :param thing_id: Thing ID to subscribe to update.
        :param on_set_property: Callback function that execute on Thing property updates.
        :param on_request_action: Callback function that execute on Thing action request.
        :param on_update: Callback function that execute on Thing schema updates.
        :raise ValueError
        :return: The thing queue name that receive the messages with the updates.
        """
        if on_set_property is None and on_request_action is None and on_update is None:
            raise ValueError

        logger.info("Thing {} subscribing", thing_id)
        thing_queue_name = f'{self._queue_prefix}.{thing_id}.{int(time.time())}'
        self._subscribed_things[thing_id] = {'queue_name': thing_queue_name}
        if on_set_property is not None:
            self.subscribe_on_set_property(thing_id, on_set_property)
        if on_request_action is not None:
            self.subscribe_on_request_action(thing_id, on_request_action)
        if on_update is not None:
            self.subscribe_on_update(thing_id, on_update)

        if self.loop_in_other_thread():
            asyncio.run_coroutine_threadsafe(self._bind_queue(thing_id, thing_queue_name), self._loop).result()
        else:
            await self._bind_queue(thing_id, thing_queue_name)

        return thing_queue_name

    async def unsubscribe(self, thing_id: str) -> NoReturn:
        """Unsubscribe Thing ID for all callback and updates.

        :param thing_id: Thing ID to unsubscribe.
        """

        if thing_id not in self._subscribed_things:
            raise ValueError("Thing not subscribed")

        thing = self._subscribed_things[thing_id]
        queue: AbstractQueue = thing['queue']

        if self.loop_in_other_thread():
            asyncio.run_coroutine_threadsafe(queue.cancel(thing['consumer_tag']), self._loop).result()
            asyncio.run_coroutine_threadsafe(queue.unbind(self._exchange), self._loop).result()
            asyncio.run_coroutine_threadsafe(queue.delete(), self._loop).result()
        else:
            await queue.cancel(thing['consumer_tag'])
            await queue.unbind(self._exchange)
            await queue.delete()
        del self._subscribed_things[thing_id]

    def subscribe_on_set_property(self, thing_id: str,
                                  on_set_property: Callable[[[str, Any]], Coroutine[NoReturn]]) -> NoReturn:
        """Subscribe the Thing ID for receive Thing property updates.

        Subscribe the Thing ID for receive Thing property updates.
        :param thing_id: Thing ID to subscribe to update.
        :param on_set_property: Callback function that execute on Thing property updates.
        """

        self._subscribed_things[thing_id]['on_set_property'] = on_set_property
        logger.info("Thing {} subscribed to on_set_property", thing_id)

    def unsubscribe_on_set_property(self, thing_id: str) -> NoReturn:
        """Unsubscribe Thing ID for on_set_property callback and updates.

        :param thing_id: Thing ID to unsubscribe.
        """

        del self._subscribed_things[thing_id]['on_set_property']
        logger.info("Thing {} unsubscribed from on_set_property", thing_id)

    def subscribe_on_request_action(self, thing_id: str,
                                    on_request_action: Callable[[[str, str, ...]], Coroutine[NoReturn]]) -> NoReturn:
        """Subscribe the Thing ID for receive Thing action request.

        Subscribe the Thing ID for receive Thing action request.
        :param thing_id: Thing ID to subscribe to update.
        :param on_request_action: Callback function that execute on Thing action request.
        """

        self._subscribed_things[thing_id]['on_request_action'] = on_request_action
        logger.info("Thing {} subscribed to on_request_action", thing_id)

    def unsubscribe_on_request_action(self, thing_id: str) -> NoReturn:
        """Unsubscribe Thing ID for on_request_action callback and updates.

        :param thing_id: Thing ID to unsubscribe.
        """

        del self._subscribed_things[thing_id]['on_request_action']
        logger.info("Thing {} unsubscribed from on_request_action", thing_id)

    def subscribe_on_update(self, thing_id: str,
                            on_update: Callable[[dict[str, Any]], Coroutine[NoReturn]]) -> NoReturn:
        """Subscribe the Thing ID for receive Thing schema updates.

        Subscribe the Thing ID for receive Thing schema updates.
        :param thing_id: Thing ID to subscribe to update.
        :param on_update: Callback function that execute on Thing schema updates.
        """

        self._subscribed_things[thing_id]['on_update'] = on_update
        logger.info("Thing {} subscribed to on_update", thing_id)

    def unsubscribe_on_update(self, thing_id: str) -> NoReturn:
        """Unsubscribe Thing ID for on_update callback and updates.

        :param thing_id: Thing ID to unsubscribe.
        """
        del self._subscribed_things[thing_id]['on_update']
        logger.info("Thing {} unsubscribed from on_update", thing_id)

    async def _bind_queue(self, thing_id: str, thing_queue_name: str) -> NoReturn:
        """Create a RabbitMQ queue and bind it to the driver exchange.

        :param thing_id: Thing ID for the bind queue.
        :param thing_queue_name: Name of the new Thing queue.
        """

        thing = self._subscribed_things[thing_id]
        queue = await self._channel.declare_queue(thing_queue_name, exclusive=True, auto_delete=True, timeout=10)
        thing['queue'] = queue
        args = {
            'x-match': 'all',
            'thingID': thing_id
        }
        await queue.bind(self._exchange, arguments=args)
        thing['consumer_tag'] = await queue.consume(self._on_message)
        logger.info("Thing {} driver queue bound: {}", thing_id, thing_queue_name)

    async def _on_message(self, message: AbstractIncomingMessage) -> NoReturn:
        """Callback function when a new message is received.

        :param message: Message coming from RabbitMQ driver exchange. Contain the data and headers.
        """

        async with message.process():
            thing_id = message.headers['thingID']
            message_type = message.headers['messageType']
            thing = self._subscribed_things[thing_id]

            body: Optional[dict[str, Any]] = json.loads(message.body) if message.body else None

            logger.info("Driver message {} {}: {}", thing_id, message_type, body)

            if message_type == "setProperty":
                if 'on_set_property' in thing:
                    on_set_property = thing['on_set_property']
                    tasks = [asyncio.create_task(on_set_property(property_id, property_value)) for
                             property_id, property_value in body.items()]
                    for task in tasks:
                        await task
            elif message_type == "requestAction":
                if 'on_request_action' in thing:
                    action_id = message.headers['actionID']
                    on_request_action = thing['on_request_action']
                    tasks = [asyncio.create_task(
                        on_request_action(action_key, action_id, action['input'] if 'input' in action else None)) for
                        action_key, action in body.items()]
                    for task in tasks:
                        await task
            elif message_type == "updateThing":
                if 'on_update' in thing:
                    await thing['on_update'](body)
