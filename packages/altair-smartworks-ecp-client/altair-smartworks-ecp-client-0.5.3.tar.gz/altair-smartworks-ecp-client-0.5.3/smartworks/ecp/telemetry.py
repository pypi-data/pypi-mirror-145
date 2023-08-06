"""Altair Smartworks Edge Compute Platform telemetry wrapper.

This script contains all the telemetry calls for the Altair Smartworks Edge
Compute Platform using async calls that increase performance. This allows
to send property updates, event data and action status.
"""

from __future__ import annotations

import asyncio
import json
import time
from typing import NoReturn, Any, Union, Optional
from urllib.parse import ParseResult

from aio_pika import Message
from loguru import logger

from .action import ActionRequestStatus
from .base_pubsub import BasePubSub
from .credentials import EdgeCredentials


class Telemetry(BasePubSub):
    """Altair Smartworks Edge Compute Platform telemetry wrapper.

    Telemetry connect to Edge Compute Platform to allow you to interact
    with SmartWorks IoT ECP telemetry exchange. Can run in background to allow calls for
    others thread without mutual block. It allows sending property updates, event data and
    action status.
    """

    def __init__(self, url: Optional[Union[str, ParseResult]] = None,
                 *,
                 credentials: Optional[EdgeCredentials] = None,
                 username: str = 'telemetry-user',
                 telemetry_exchange_name: str = 'ase.exchange.telemetry',
                 **kwargs):
        """
        :param url: if present, used this to initialize connection to RabbitMQ server.
        :param credentials: if url not present, use these credentials to connect to RabbitMQ server.
        :param username: if url and credential not present, use this username to connect to RabbitMQ server.
        :param telemetry_exchange_name: Name of the telemetry exchange to connect to RabbitMQ server.
        """

        super().__init__(url, credentials=credentials, username=username, exchange_name=telemetry_exchange_name,
                         **kwargs)

    async def publish_properties(self, thing_id: str, properties: dict[str, Any]) -> NoReturn:
        """Send Thing property status to the Edge

        :param thing_id: The Thing ID of the properties.
        :param properties: Dict like json serializable object containing the property names and its values.
        """

        headers = {
            'messageType': 'propertyStatus',
            'thingID': thing_id
        }
        body = {
            'thingID': thing_id,
            'data': properties
        }
        await self._publish_message(headers, body)

    async def publish_action_status(self, thing_id: str,
                                    action_key: str, action_id: str, action_status: ActionRequestStatus) -> NoReturn:
        """Send Thing action status to the Edge

        :param thing_id: The Thing ID of the action.
        :param action_key: The action key or name
        :param action_id: The action call ID.
        :param action_status: The action status.
        """

        headers = {
            'messageType': 'actionStatus',
            'thingID': thing_id
        }
        body = {
            'thingID': thing_id,
            'data': {
                action_key: {
                    'status': action_status.value,
                    'href': f'/things/{thing_id}/actions/{action_key}/{action_id}'
                }
            }
        }
        await self._publish_message(headers, body)

    async def publish_event(self, thing_id: str, event_key: str, event_data: Any) -> NoReturn:
        """Send an event to the Edge

        :param thing_id: The Thing ID of the event.
        :param event_key: The event key or name.
        :param event_data: The event data. It can be anything as long as it's json serializable.
        """

        headers = {
            'messageType': 'event',
            'thingID': thing_id
        }
        body = {
            'thingID': thing_id,
            'data': {
                event_key: {
                    'data': event_data
                }
            }
        }
        await self._publish_message(headers, body)

    async def _publish_message(self, headers: dict[str, Any], body: dict[str, Any]) -> NoReturn:
        """Send telemetry data to the Edge

        :param headers: The message headers that contains the messageType and the thingID. The publishTag will be added.
        :param body: The message body containing the thingID and the proper data. The timestamp will be added.
        """

        headers['publishTag'] = 'raw'
        body['timestamp'] = round(time.time())

        # Serialize the body if it is a dict object-
        if isinstance(body, dict):
            body = json.dumps(body)

        message = Message(body.encode('UTF-8'), headers=headers)

        # Run publish message in the Thread with a safe call if it is running on a different loop
        # on different thread.
        if self.loop_in_other_thread():
            asyncio.run_coroutine_threadsafe(self._exchange.publish(message, '', timeout=5), self._loop).result()
        else:
            await self._exchange.publish(message, '', timeout=5)

        logger.info("Published {}: {}", headers, body)
