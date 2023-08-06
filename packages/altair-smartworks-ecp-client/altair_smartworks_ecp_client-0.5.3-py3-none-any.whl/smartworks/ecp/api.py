"""Altair Smartworks Edge Compute Platform API wrapper.

This script contains all the API calls for the Altair Smartworks Edge Compute Platform
using async calls that increase performance.
"""

from __future__ import annotations

import asyncio
import random
import string
import time
import uuid
from asyncio.futures import Future
from json import JSONDecodeError
from typing import NoReturn, Any, Union, Optional, Type, Iterable
from urllib.parse import ParseResult

import orjson
from aio_pika import Message
from aio_pika.abc import AbstractQueue, AbstractIncomingMessage
from loguru import logger

from .action import ActionRequestStatus, ActionRequest
from .base_pubsub import BasePubSub
from .event import EventRequest
from .health import EdgeServiceHealth
from .label import Label
from .thing import Thing


class EdgeApi(BasePubSub):  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """Altair Smartworks Edge Compute Platform API wrapper.

    EdgeAPI connect to Edge Compute Platform to allow you to interact
    with SmartWorks IoT ECP API. Can run in background to allow calls for
    others thread without mutual block.
    """

    @staticmethod
    def _process_status_code(status_code: int, msg: Optional[str] = None) -> Optional[ValueError]:
        """Check status code.

        Check if the status code if valid and raise a ValueError if the code is not successfully like 400 errors
        :param status_code: The satus code to process
        :raise: ValueError with the error description if the status_code is an error
        """
        error = None
        if status_code == 401:
            error = "401 Access token is missing or invalid."
        elif status_code == 404:
            error = "404 Resource not found."
        elif status_code == 408:
            error = "408 Request has timed out."
        elif status_code == 409:
            error = "409 Request caused a conflict."
        if error is not None and msg is not None:
            error = f"{error} {msg}"
        return error

    @staticmethod
    def _parse_requests(requests: list[dict[str, Any]],
                        request_cls: Type[Union[ActionRequest, EventRequest]]) -> dict[str, list[Union[ActionRequest,
                                                                                                       EventRequest]]]:
        """Parse the requests for list of dict requests to dict of list request by request key.

        :param requests: A list of dict requests to parse.
        :param request_cls: The class of the request.
        :return: A dict of list requests by request key.
        """

        res = {}
        for request in requests:
            for request_key, request_dict in request.items():
                request_dict = request_cls.from_ecp_dict(request_key, request_dict)
                if request_key in res:
                    res[request_key].append(request_dict)
                else:
                    res[request_key] = [request_dict]
        return res

    def __init__(self,
                 url: Optional[Union[str, ParseResult]] = None,
                 *,
                 username: str = 'api-user',
                 api_exchange_name: str = 'ase.exchange.api', callback_queue_name: str = 'ase.callback.api',
                 **kwargs):
        """
        :param url: If present, use this URL with schema, host, port, username and password to connect to RabbitMQ.
        :param username: API username for ECP RabbitMQ exchange.
        :param api_exchange_name: API RabbitMQ exchange name.
        :param callback_queue_name: API RabbitMQ callback queue use to receive response from API exchange request.
        """

        super().__init__(url, username=username, exchange_name=api_exchange_name, **kwargs)

        self._callback_queue_name = callback_queue_name
        self._queue: Optional[AbstractQueue] = None
        self._consumer_tag: Optional[str] = None

        self._futures: dict[str, Future] = {}

    async def _connect(self, loop=None) -> NoReturn:
        await super()._connect(loop)

        # Generate queue name for the ECP API response with the prefix
        queue_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        self._queue = await self._channel.declare_queue(f'{self._callback_queue_name}.{queue_name}.{int(time.time())}',
                                                        exclusive=True, auto_delete=True, timeout=10)
        self._consumer_tag = await self._queue.consume(self._on_message)

        return self

    async def _close(self) -> NoReturn:
        # Cancel the queue, unbind it from the API exchange and delete it
        await self._queue.cancel(self._consumer_tag)
        await self._queue.delete()

        self._consumer_tag = None
        self._queue = None

        await super()._close()

    async def _on_message(self, message: AbstractIncomingMessage) -> NoReturn:
        """Process incoming message.

        Process the incoming message from the queue checking the status code and setting the Future with the message
        deserialized.
        :param message: The incoming message from the queue.
        """

        async with message.process():
            if message.correlation_id not in self._futures:
                return

            future = self._futures.pop(message.correlation_id)

            # Check if response is and error and process it.
            if message.headers is not None and 'statusCode' in message.headers:
                exception_msg = self._process_status_code(message.headers['statusCode'], msg=message.body.decode())
                if exception_msg is not None:
                    future.set_exception(ValueError(exception_msg))
                    return

            try:
                body = orjson.loads(message.body or 'null')
                logger.info("Received API message from {} ({}): {}",
                            message.headers['messageType'] if 'messageType' in message.headers else 'error',
                            message.correlation_id, body)

                if body is None:
                    future.set_result(None)
                    return

                if 'error' in body:
                    error = body['error']
                    status_code = error['status']
                    error_msg = error['message']
                    exception_msg = self._process_status_code(status_code, msg=error_msg)
                    if exception_msg is None:
                        exception_msg = f"{status_code} {error_msg}"
                    future.set_exception(ValueError(exception_msg))
                    return
                future.set_result(body)  # Set the Future result to wake up the API request await Future.
            except JSONDecodeError as json_decode_exception:
                future.set_exception(json_decode_exception)

    async def _publish_threadsafe(self, method: str, href: str,
                                  body: Union[str, dict[str, Any]] = '') -> Any:
        """
        Used to call publish if the call is from another Thread or loop from the one who create the connection.
        Publish an ECP API request with the specific HTTP method to the href and the body.

        :param method: The HTTP method of the request.
        :param href: The href of the ECP API endpoint.
        :param body: If necessary, the request body with the corresponding data.
        :return: The response of the ECP API endpoint.
        """

        if self.loop_in_other_thread():
            return asyncio.run_coroutine_threadsafe(self._publish(method, href, body), self._loop).result()
        return await self._publish(method, href, body)

    async def _publish(self, method: str, href: str,
                       body: Union[str, dict[str, Any]] = '') -> Any:
        """Publish an ECP API request.

        Publish an ECP API request with the specific HTTP method to the href and the body.
        :param method: The HTTP method of the request.
        :param href: The href of the ECP API endpoint.
        :param body: If necessary, the request body with the corresponding data.
        :return: The response of the ECP API endpoint.
        """
        # If the body is a dict instance, serialize it to json string.
        body = orjson.dumps(body) if body is not None and isinstance(body, dict) else body.encode()
        correlation_id = str(uuid.uuid4())  # Create a new correlation id for the response.
        future = asyncio.Future()  # Create a Future to return when the response result is set.
        self._futures[correlation_id] = future  # Save the future in a dict with the correlation id.

        message = Message(
            body,
            headers={'requestMethod': method, 'href': href, 'swx-cloud-sync': True},
            content_type='application/json',
            content_encoding='UTF-8',
            correlation_id=correlation_id,  # Match the incoming message response with this request
            reply_to=self._queue.name,
        )
        await self._exchange.publish(message, '', timeout=5)  # Publish the message in the API exchange.

        if body:
            logger.info("Sent API message ({}) requesting {} {}: {}", correlation_id, method, href, body)
        else:
            logger.info("Sent API message ({}) requesting {} {}", correlation_id, method, href)

        return await future  # Wait until the Future result is set.

    async def things(self, thing_ids: Optional[Iterable[str]] = None, *, thing_cls: Type[Thing] = Thing) -> list[Thing]:
        """Get Things from the Edge.

        Get all the Things from the Edge with the specific thing_cls in @type or get the specific Things if thing_ids
        is set.
        :param thing_ids: Thing ids to get.
        :param thing_cls: Return only the objects of this thing_cls in @type.
        :return: A list with all the Things that matched the thing_cls and thing_ids if set.
        """

        # Check if the loop is in running in other thread.
        if self.loop_in_other_thread():
            return asyncio.run_coroutine_threadsafe(self._things(thing_ids, thing_cls=thing_cls), self._loop).result()
        return await self._things(thing_ids, thing_cls=thing_cls)

    async def _things(self, thing_ids: Optional[Iterable[str]] = None, *,
                      thing_cls: Type[Thing] = Thing) -> list[Thing]:
        if thing_ids:
            # Get all the things with the thing_ids
            tasks = [self._loop.create_task(self._thing(thing_id, thing_cls=thing_cls)) for thing_id in thing_ids]
            # Create task and await later to improve asyncio performance
            return [await task for task in tasks]

        # Get all the Things from the Edge and check if thing_cls is in @type if thing_cls is not Thing
        things = [thing for thing in await self._publish('GET', '/things') if
                  ('@type' in thing and thing_cls.__name__ in thing['@type']) or thing_cls == Thing]

        tasks = [(thing, self._loop.create_task(self._thing_properties(thing['uid']))) for thing in things]
        # Create task and await later to improve asyncio performance
        return [thing_cls.from_ecp_dict(thing, properties=await task) for thing, task in tasks]

    async def add_thing(self, thing: Thing) -> Thing:
        """Add a new Thing to the Edge and to the Altair SmartWorks cloud.

        Add a new Thing to the Edge and synchronized it with the Altair SmartWorks Iot cloud if possible.
        :param thing: The thing to add.
        :return: The same Thing with updated attributes like uid.
        """

        updated_thing_dict = await self._publish_threadsafe('POST', "/things", body=thing.to_ecp_dict())
        return await thing.on_update(updated_thing_dict)

    async def thing(self, thing_id: str, *, thing_cls: Type[Thing] = Thing) -> Thing:
        """Get the Thing from the Edge with the specific Thing ID.

        Get the Thing from the Edge with the specific Thing ID and create a Thing object of type thing_cls only if
        thing_cls is in the @type of the Thing.
        :param thing_id: The Thing ID of the Thing to get.
        :param thing_cls: The thing_cls of the Thing.
        :return: The Thing object of type thing_cls and thing_id or None if no Thing satisfy the thing_id and thing_cls.
        """

        if self.loop_in_other_thread():
            return asyncio.run_coroutine_threadsafe(self._thing(thing_id, thing_cls=thing_cls), self._loop).result()
        return await self._thing(thing_id, thing_cls=thing_cls)

    async def _thing(self, thing_id: str, *, thing_cls: Type[Thing] = Thing) -> Thing:
        thing = await self._publish('GET', f'/things/{thing_id}')
        properties = await self._thing_properties(thing_id) if ('@type' in thing and thing_cls.__name__
                                                                in thing['@type']) or thing_cls == Thing else None
        return thing_cls.from_ecp_dict(thing, properties=properties)

    async def update_thing(self, thing: Thing) -> Thing:
        """Update Thing scheme.

        Update the Thing scheme in the Edge and synchronize it with the Altair SmartWorks Iot cloud.
        :param thing: The Thing to update.
        :return: The same Thing with updated attributes.
        """

        updated_thing_dict = await self._publish_threadsafe('PUT', f"/things/{thing.uid}",
                                                            body=thing.to_ecp_dict(include_all=True))
        del updated_thing_dict['uid']
        del updated_thing_dict['id']
        return await thing.on_update(updated_thing_dict)

    async def delete_thing(self, thing: Union[str, Thing]) -> bool:
        """Delete a Thing from the Edge.

        :param thing: The Thing ID or Thing object to delete from the Edge,
        :return: True if success else False
        """

        thing_id = thing.uid if isinstance(thing, Thing) else thing
        return await self._publish_threadsafe('DELETE', f'/things/{thing_id}')

    async def thing_properties(self, thing: Union[str, Thing]) -> dict[str, Any]:
        """Get Thing property keys and values.

        :param thing: Thing ID ot Thing object to get properties.
        :return: A dict with the Thing properties.
        """

        if self.loop_in_other_thread():
            return asyncio.run_coroutine_threadsafe(self._thing_properties(thing), self._loop).result()
        return await self._thing_properties(thing)

    async def _thing_properties(self, thing: Union[str, Thing]) -> dict[str, Any]:
        thing_id = thing.uid if isinstance(thing, Thing) else thing
        return await self._publish('GET', f'/things/{thing_id}/properties')

    async def update_thing_properties(self, thing: Thing) -> dict[str, Any]:
        """Update Thing property values from the Edge.

        :param thing: The Thing object to update its values from the Edge.
        :return: The updated properties in a dict format.
        """

        return await self._publish_threadsafe('PUT', f'/things/{thing.uid}/properties',
                                              body=thing.edge_properties_dict())

    async def thing_property(self, thing_id: str, property_id: str) -> Any:
        """Get Thing property value.

        :param thing_id: Thing ID that contains the property.
        :param property_id: Property ID to get the value.
        :return: The value of the Thing property.
        """

        return next(iter((await self._publish_threadsafe('GET',
                                                         f'/things/{thing_id}/properties/{property_id}')).values()))

    async def update_thing_property(self, thing_id: str, property_id: str,
                                    property_value: Optional[Any] = None) -> Any:
        """Update Thing property value

        :param thing_id: Thing ID with the property.
        :param property_id: Property ID to update.
        :param property_value: Property value.
        :return: The value of the updated Thing property.
        """

        # Only can be one item in the dict response.
        return next(iter((await self._publish_threadsafe('PUT',
                                                         f'/things/{thing_id}/properties/{property_id}',
                                                         body={property_id: property_value})).values()))

    async def thing_actions(self, thing_id: str) -> dict[str, list[ActionRequest]]:
        """Get Thing actions request history.

        :param thing_id: Thing ID to get all action request history.
        :return: A dict with action_key as keys and list of ActionRequestResponse as values.
        """
        action_requests = await self._publish_threadsafe('GET', f'/things/{thing_id}/actions')
        if action_requests:
            action_requests = self._parse_requests(action_requests, ActionRequest)
        return action_requests

    async def request_thing_action(self, thing_id: str,
                                   action_key: str,
                                   inputs: Any) -> ActionRequest:
        """Request a Thing action to be performed.

        :param thing_id: Thing ID with the action to request.
        :param action_key: Action key to request.
        :param inputs: The input values of the actions. Must be json serializable.
        :return: ActionRequest object with the action request ID.
        """

        action_requests = await self._publish_threadsafe('POST', f'/things/{thing_id}/actions/{action_key}',
                                                         body={action_key: {'input': inputs}})
        action_key, action_request = next(iter(action_requests.items()))
        return ActionRequest.from_ecp_dict(action_key, action_request)

    async def thing_action(self, thing_id: str, action_key: str) -> list[ActionRequest]:
        """List all history of requests for an Action of a Thing.

        :param thing_id: Thing ID with the action to list history.
        :param action_key: Action key to list history.
        :return: A list of ActionRequest.
        """

        action_requests = await self._publish_threadsafe('GET', f'/things/{thing_id}/actions/{action_key}')
        if action_requests:
            action_requests = [ActionRequest.from_ecp_dict(action_key, next(iter(action_request.values())))
                               for action_request in action_requests]
        return action_requests

    async def show_thing_action(self, thing_id: str,
                                action_key: str,
                                action_id: str) -> ActionRequest:
        """Show an existing Thing action request.

        :param thing_id: Thing ID with the action request to show.
        :param action_key: Action key to show.
        :param action_id: The action ID to show.
        :return: ActionRequest with the request.
        """

        action_request = await self._publish_threadsafe('GET', f'/things/{thing_id}/actions/{action_key}/{action_id}')
        return ActionRequest.from_ecp_dict(action_key, action_request)

    async def response_thing_action(self, thing_id: str,
                                    action_key: str,
                                    action_id: str,
                                    status: ActionRequestStatus) -> ActionRequest:
        """Update an existing Thing action status.

        :param thing_id: Thing ID with the action to update.
        :param action_key: Action key to update.
        :param action_id: The request action ID to update.
        :param status: The status of the action request.
        :return: The new ActionRequest with the request.
        """

        action_request = await self._publish_threadsafe('PUT', f'/things/{thing_id}/actions/{action_key}/{action_id}',
                                                        body={action_id: {'status': status.value}})
        return ActionRequest.from_ecp_dict(action_key, action_request)

    async def delete_thing_action(self, thing_id: str, action_key: str, action_id: str) -> NoReturn:
        """Cancels an existing action if pending or deletes when finished or cancelled.

        :param thing_id: Thing ID with the action to cancel or delete.
        :param action_key: Action key to cancel or delete.
        :param action_id: Action id to cancel or delete.
        """

        await self._publish_threadsafe('DELETE', f'/things/{thing_id}/actions/{action_key}/{action_id}')

    async def thing_events(self, thing_id: str) -> dict[str, list[EventRequest]]:
        """List all history of request for all Events of a Thing.

        :param thing_id: Thing ID to list of his request Events.
        :return: A dict of list EventRequest by event key.
        """

        return self._parse_requests(await self._publish_threadsafe('GET', f'/things/{thing_id}/events'), EventRequest)

    async def thing_event(self, thing_id: str, event_key: str) -> list[EventRequest]:
        """List all history of request for a Thing events.

        :param thing_id: Thing ID to list of his request Events.
        :param event_key: The event key to list his requests.
        :return: A list of EventRequest
        """

        return [EventRequest.from_ecp_dict(event_key, next(iter(event_request.values())))
                for event_request in await self._publish_threadsafe('GET', f'/things/{thing_id}/events/{event_key}')]

    async def show_thing_event(self, thing_id: str, event_key: str, event_id: str) -> EventRequest:
        """Show an existing Thing event request.

        :param thing_id: Thing ID with the event request to show.
        :param event_key: Event key to show
        :param event_id: The event id to show.
        :return: A EventRequest with the Thing event request.
        """

        event_request = await self._publish_threadsafe('GET', f'/things/{thing_id}/events/{event_key}/{event_id}')
        return EventRequest.from_ecp_dict(event_key, event_request)

    async def delete_thing_event(self, thing_id: str, event_key: str, event_id: str) -> NoReturn:
        """Deletes an existing Thing event.

        :param thing_id: Thing ID with the action to cancel or delete.
        :param event_key: Event key to delete.
        :param event_id: The event id to delete.
        """

        await self._publish_threadsafe('DELETE', f'/things/{thing_id}/events/{event_key}/{event_id}')

    async def labels(self) -> dict[str, Label]:
        """List all labels.

        :return: A dict with all labels in Label by label id.
        """

        return {label_dict['labelId']: Label(**label_dict)
                for label_dict in await self._publish_threadsafe('GET', '/support/labels')}

    async def add_label(self, label: Label) -> Label:
        """Add a new label.

        :param label: The new Label to add.
        :return: label with updated attributes.
        """

        label.on_update(await self._publish_threadsafe('POST', "/support/labels", body=label.to_ecp_dict()))
        return label

    async def label(self, label_id: str) -> Label:
        """Get a label.

        :param label_id: Label id to get.
        :return: Label with label_id
        """

        return Label(**(await self._publish_threadsafe('GET', f'/support/labels/{label_id}')))

    async def update_label(self, label: Label) -> Label:
        """Update an existing Label.

        :param label: Label to update.
        :return: Label with updated attributes.
        """

        label.on_update(await self._publish_threadsafe('PUT', f"/support/labels/{label.uid}",
                                                       body=label.to_ecp_dict()))
        return label

    async def delete_label(self, label_id: str) -> NoReturn:
        """Delete an existing Label.

        :param label_id: Label id to delete.
        """

        await self._publish_threadsafe('DELETE', f'/support/labels/{label_id}')

    async def enable_thing_cloud_sync(self, thing_id: str,
                                      mqtt_url: str = 'tcp://mqtt.swx.altairone.com:1883') -> bool:
        """Enable the synchronization with the Smartworks Iot Cloud for the Thing.

        :param thing_id: The Thing ID to enable the synchronization.
        :param mqtt_url: The URL of the mqtt for the synchronization.
        :return: True if success and in other case False
        """

        return await self._publish_threadsafe('PUT', f'/support/smartworks/thingConnections/{thing_id}',
                                              body={'connectionURL': mqtt_url})

    async def disable_thing_cloud_sync(self, thing_id: str,
                                       mqtt_url: str = 'tcp://mqtt.swx.altairone.com:1883') -> bool:
        """Disable the synchronization with the Smartworks Iot Cloud for the Thing.

        :param thing_id: The Thing ID to disable the synchronization.
        :param mqtt_url: The URL of the mqtt for the synchronization.
        :return: True if success and in other case False
        """

        return await self._publish_threadsafe('DELETE', f'/support/smartworks/thingConnections/{thing_id}',
                                              body={'connectionURL': mqtt_url})

    async def services_health(self) -> dict[str, EdgeServiceHealth]:
        """List health status of Edge Compute Platform services.

        :return: A dict with EdgeHealth by service key
        """

        edge_health_dicts = await self._publish_threadsafe('GET', '/health/services')
        return {edge_health_dict['key']: EdgeServiceHealth(**edge_health_dict)
                for edge_health_dict in edge_health_dicts}

    async def service_health(self, service_id: str) -> EdgeServiceHealth:
        """Show an existing health status of a service.

        :param service_id: Service ID to show.
        :return: EdgeHealth with the service health.
        """

        edge_health_dict = await self._publish_threadsafe('GET', f'/health/services/{service_id}')
        return EdgeServiceHealth(**edge_health_dict)

    async def configure_service_logs(self, service_id: str, log_level: str, pretty: bool, color: bool) -> NoReturn:
        """Update the logger configuration of a service.

        :param service_id: Service ID to update his logger.
        :param log_level: Log level.
        :param pretty: Pretty print.
        :param color: Print with color.
        """

        await self._publish_threadsafe('PUT', f'/logging/services/{service_id}', body={
            'level': log_level,
            'pretty': pretty,
            'color': color
        })
