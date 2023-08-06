"""This script contains the base classes for creating a IoT Thing.

This script contains te base class for creating a IoT Thing based on the
Altair SmartWorks IoT Thing schema. It provides the class for creating a
Thing property, a Thing action and a Thing event. These classes represent
the schema and in order to implement it you must inherit from the Thing
class and create your Thing with your properties as attributes and actions
and events as methods.
"""

from __future__ import annotations

import asyncio
import functools
from asyncio import AbstractEventLoop, Handle
from builtins import setattr
from datetime import datetime
from threading import Thread, Event
from typing import Any, NoReturn, Union, Optional, Callable, Iterable, ClassVar
from urllib.parse import ParseResult

from pydantic import BaseModel, Field

from .action import ActionRequestStatus
from .telemetry import Telemetry


class ThingLink(BaseModel):
    """ThingLink represent the link that an IoT Thing could have.

    :var rel: Link name.
    :var href: The link.
    """

    rel: str
    href: str


class ThingPropertyBase(BaseModel):
    """The Base property is the base for all the properties, and it is the null type.

    :var uid: Thing property ID.
    :var title: Thing property title.
    :var description: Thing property description.
    :var unit: Thing property unit.
    :var read_only: Indicates if the property is read only. If it is, no modifications are allowed.
    :var type: The type of the property.
    """

    uid: str = Field(..., alias='id', compare=True, hash=True)
    title: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    read_only: bool = Field(False, alias='readOnly')
    type: str = Field('null', const=True)

    @classmethod
    def parse_ecp_dict(cls, edge_api_properties_dict: dict[str, Any]) -> dict[str, Any]:
        """Parse the ECP API properties dict key names with the Thing Property attributes format names.

        :param edge_api_properties_dict: The ECP API dict containing the Thing Property values.
        :return: The parsed ECP API properties dict.
        """

        del edge_api_properties_dict['type']  # Delete type. Can't be changed.
        return edge_api_properties_dict

    def to_ecp_dict(self) -> dict[str, Any]:
        """Convert to Altair Smartworks ECP dict format."""

        return self.dict(exclude={'uid'}, exclude_unset=True)

    def check(self, value: Any) -> NoReturn:
        """Check if the value is valid for this property.

        :param value: The value to check if it is valid.
        :raise ValueError: If the value is not valid with the error.
        """
        if value is not None:
            raise ValueError(f"{self.uid} must be None")


class _ThingPropertyBaseNumber(ThingPropertyBase):
    """Base class for number Properties with maximum and minimum value.

    :var maximum: The maximum value that this property can be. Exclusive maximum.
    :var minimum: The minimum value that this property can be. Exclusive minimum.
    """

    maximum: Optional[Union[int, float]] = None
    minimum: Optional[Union[int, float]] = None

    def check(self, value: Union[int, float]) -> NoReturn:
        """Check if the value is between the maximum and minimum.

        :param value: The value to check if it is valid.
        :raise ValueError: If the value isn't between maximum and minimum if they are not None.
        """
        if value is None:
            raise ValueError("value can not be None")
        if self.maximum is not None and value > self.maximum:
            raise ValueError(f"{self.uid} must be lower than {self.maximum}")
        if self.minimum is not None and value < self.minimum:
            raise ValueError(f"{self.uid} must be higher than {self.minimum}")


class ThingPropertyFloat(_ThingPropertyBaseNumber):
    """Float property"""

    type: str = Field('float', const=True)


class ThingPropertyInteger(_ThingPropertyBaseNumber):
    """Integer property"""

    type: str = Field('integer', const=True)


class ThingPropertyString(ThingPropertyBase):
    """String property"""

    type: str = Field('string', const=True)


class ThingPropertyBool(ThingPropertyBase):
    """Bool property"""

    type: str = Field('boolean', const=True)


class ThingPropertyObject(ThingPropertyBase):
    """Object property that could contain any Thing property in a dict.

    :var properties: The dict with all the properties that has.
    """

    properties: dict[str, ThingPropertyBase] = Field(default_factory=dict)
    type: str = Field('object', const=True)

    @classmethod
    def parse_ecp_dict(cls, edge_api_properties_dict: dict[str, Any]) -> dict[str, Any]:
        super().parse_ecp_dict(edge_api_properties_dict)
        if 'properties' in edge_api_properties_dict:
            edge_api_properties_dict['properties'] = {
                property_id: thing_property_from_ecp_dict(property_id, property_) for
                property_id, property_ in edge_api_properties_dict['properties'].items()}
        return edge_api_properties_dict

    def to_ecp_dict(self) -> dict[str, Any]:
        edge_property = super().to_ecp_dict()
        edge_property['properties'] = {property_id.replace(' ', '_'): thing_property.to_ecp_dict() for
                                       property_id, thing_property in self.properties.items()}
        return edge_property


class ThingPropertyArray(ThingPropertyBase):
    """Array property that could contain any Thing property in a list.

    :var items: The list with the Thing properties that has.
    :var max_items: The number of maximum items that items could have.
    :var min_items: The number of minimum items that items could have.
    """

    items: ThingPropertyBase
    max_items: Optional[int] = Field(None, alias='maxItems')
    min_items: Optional[int] = Field(None, alias='minItems')
    type: str = Field('array', const=True)

    @classmethod
    def parse_ecp_dict(cls, edge_api_properties_dict: dict[str, Any]) -> dict[str, Any]:
        super().parse_ecp_dict(edge_api_properties_dict)
        if 'items' in edge_api_properties_dict:
            edge_api_properties_dict['items'] = [thing_property_from_ecp_dict('', thing_property)
                                                 for thing_property in edge_api_properties_dict['items']]
        return edge_api_properties_dict

    def to_ecp_dict(self) -> dict[str, Any]:
        edge_property = super().to_ecp_dict()
        edge_property['items'] = self.items.to_ecp_dict()
        return edge_property

    def check(self, value: list[Any]) -> NoReturn:
        """Check if the value length is between the maximum and minimum.

        :param value: The value to check if it is valid.
        :raise ValueError: If the value length isn't between max_items and min_items if they are not None.
        """

        if value is None:
            raise ValueError("value can not be None")
        if self.max_items is not None and len(value) > self.max_items:
            raise ValueError(f"{self.uid} length must be lower than {self.max_items}")
        if self.min_items is not None and len(value) < self.min_items:
            raise ValueError(f"{self.uid} length must be lower than {self.min_items}")


def thing_property_from_ecp_dict(edge_property_id: str,
                                 edge_api_properties_dict: dict[str, Any]) -> ThingPropertyBase:
    """Convert the ECP API dict into the corresponding Thing property based on type key.

    :param edge_property_id: Thing property id.
    :param edge_api_properties_dict: Thing property schema dict from ECP API.
    :return: The object representing the Thing property with the corresponding Thing property.
    """

    edge_property_type = edge_api_properties_dict['type']
    if edge_property_type == 'number':
        return ThingPropertyFloat(id=edge_property_id,
                                  **ThingPropertyFloat.parse_ecp_dict(edge_api_properties_dict))
    if edge_property_type == 'integer':
        return ThingPropertyInteger(id=edge_property_id,
                                    **ThingPropertyInteger.parse_ecp_dict(
                                        edge_api_properties_dict))
    if edge_property_type == 'string':
        return ThingPropertyString(id=edge_property_id,
                                   **ThingPropertyString.parse_ecp_dict(edge_api_properties_dict))
    if edge_property_type == 'boolean':
        return ThingPropertyBool(id=edge_property_id,
                                 **ThingPropertyBool.parse_ecp_dict(edge_api_properties_dict))
    if edge_property_type == 'object':
        return ThingPropertyObject(id=edge_property_id,
                                   **ThingPropertyObject.parse_ecp_dict(edge_api_properties_dict))
    if edge_property_type == 'array':
        return ThingPropertyArray(id=edge_property_id,
                                  **ThingPropertyArray.parse_ecp_dict(edge_api_properties_dict))
    return ThingPropertyBase(id=edge_property_id,
                             **ThingPropertyBase.parse_ecp_dict(edge_api_properties_dict))


class ThingAction(BaseModel):
    """Represent the schema of a Thing action.

    :var key: Thing action key.
    :var title: Thing action title.
    :var description: Thing action description.
    :var input: Thing action input data as a Thing property.
    """

    key: str = Field(compare=True, hash=True)
    title: Optional[str] = None
    description: Optional[str] = None
    input: Optional[ThingPropertyBase] = None

    @classmethod
    def from_ecp_dict(cls, action_key: str, edge_api_action_dict: dict[str, Any]):
        """Convert the ECP API dict into the corresponding Thing action.

        :param action_key: Thing action key.
        :param edge_api_action_dict: Thing action schema dict from ECP API.
        :return: The object representing the Thing action.
        """

        if 'input' in edge_api_action_dict:
            edge_api_action_dict['input'] = thing_property_from_ecp_dict(action_key, edge_api_action_dict['input'])
        return cls(key=action_key, **edge_api_action_dict)

    def to_ecp_dict(self) -> dict[str, Any]:
        """Convert to Altair Smartworks ECP dict format."""

        return self.dict(include={'title', 'description', 'input'}, exclude_unset=True)


class ThingEvent(BaseModel):
    """Represent the schema of a Thing event.

    :var key: Thing event key.
    :var title: Thing event title.
    :var description: Thing event description.
    :var data: Thing event output data as a Thing property.
    """

    key: str = Field(compare=True, hash=True)
    title: Optional[str] = None
    description: Optional[str] = None
    data: Optional[ThingPropertyBase] = None

    @classmethod
    def from_ecp_dict(cls, event_key: str, edge_api_event_dict: dict[str, Any]):
        """Convert the ECP API dict into the corresponding Thing event.

        :param event_key: Thing event key.
        :param edge_api_event_dict: Thing action schema dict from ECP API.
        :return: The object representing the Thing event.
        """

        if 'data' in edge_api_event_dict:
            edge_api_event_dict['data'] = thing_property_from_ecp_dict(event_key, edge_api_event_dict['data'])
        return cls(key=event_key, **edge_api_event_dict)

    def to_ecp_dict(self) -> dict[str, Any]:
        """Convert to Altair Smartworks ECP dict format."""

        return self.dict(include={'title', 'description', 'data'}, exclude_unset=True)


class Thing:  # pylint: disable=too-many-instance-attributes,too-few-public-methods,too-many-public-methods
    """Base class to crete a Thing. It contains the method to update the properties,
    update the Thing schema and execute method as Thing actions. It also has the ability to send
    properties values to the telemetry, send basic event like Error event and update the action
    status and rollback if the property updated was blocked. It contains the base attributes of a
    Thing like the uid, the href and a dict that represent the properties, actions and events that
    the Thing has. Inherit this class to create your own Thing."""

    EDGE_DATETIME_FORMAT: ClassVar[str] = '%Y-%m-%dT%H:%M:%SZ'

    _PARSE_EDGE_KEYS: ClassVar[dict[str, str]] = {
        'space': '_space',
        'uid': '_uid',
        'id': '_thing_id',
        'href': '_href',
        'modified': '_modified',
    }
    _BLOCKED_EDGE_KEYS: ClassVar[set[str]] = {'created'}

    _PARSE_EDGE_PROPERTIES: dict[str, str] = {}
    _BLOCKED_EDGE_PROPERTIES: set[str] = set()

    _callback_function_loop: Optional[AbstractEventLoop] = None
    _callback_function_thread: Optional[Thread] = None
    _callback_function_thread_started_event = Event()

    @classmethod
    def run(cls) -> NoReturn:
        """Start the thread where the scheduled function will run."""

        if cls.is_running():
            cls.stop()
        cls._callback_function_loop = asyncio.new_event_loop()
        cls._callback_function_thread = Thread(target=Thing._callback_function_run)
        cls._callback_function_thread.start()
        cls._callback_function_thread_started_event.wait()

    @classmethod
    def stop(cls, join: bool = True) -> NoReturn:
        """Stop the thread and loop that schedule the functions."""

        asyncio.run_coroutine_threadsafe(cls._callback_function_loop.shutdown_asyncgens(),
                                         cls._callback_function_loop).result()
        cls._callback_function_loop.call_soon_threadsafe(cls._callback_function_loop.stop)
        if cls._callback_function_thread is not None and cls._callback_function_thread.is_alive() and join:
            cls._callback_function_thread.join()

    @classmethod
    def is_running(cls) -> bool:
        """Return if the Thread with schedule functions is running or not."""

        return cls._callback_function_thread is not None and cls._callback_function_thread.is_alive() and \
               cls._callback_function_loop is not None and cls._callback_function_loop.is_running()

    @classmethod
    def _callback_function_run(cls):
        """Execute this function when a thread start to create an asyncio loop."""

        asyncio.set_event_loop(cls._callback_function_loop)
        cls._callback_function_thread_started_event.set()
        cls._callback_function_loop.run_forever()
        cls._callback_function_loop = None
        cls._callback_function_thread = None

    @classmethod
    def default_properties(cls) -> dict[str, ThingPropertyBase]:
        """Get the default properties for a Thing which properties parameter is None"""

        return {
            'thing_status': ThingPropertyString(id='thing_status', title="Status", description="Status"),
        }

    @classmethod
    def default_actions(cls) -> dict[str, ThingAction]:
        """Get the default actions for a Thing which actions parameter is None"""

        return {}

    @classmethod
    def default_events(cls) -> dict[str, ThingEvent]:
        """Get the default events for a Thing which events parameter is None"""

        return {
            'errors': ThingEvent(key='errors', title="Errors", description="Device's errors",
                                 data=ThingPropertyString(id='error', title="Error",
                                                          description="Error description")),
            'warnings': ThingEvent(key='warnings', title="Warnings", description="Device's warnings",
                                   data=ThingPropertyString(id='warning', title="Warning",
                                                            description="Warning description")),
            'info': ThingEvent(key='info', title="Info", description="Device's info",
                               data=ThingPropertyString(id='info', title="Info", description="Info description"))
        }

    @staticmethod
    def _parse_edge_api_links(links: list[dict[str, str]]) -> list[ThingLink]:
        """Parse ECP API Thing links into ThingLink objects.

        :param links: list of ECP API Thing links.
        :return: list of ThingLinks with the information from link.
        """

        return [ThingLink(href=link['href'], rel=link['rel']) for link in links]

    @staticmethod
    def _parse_edge_api_properties(properties: dict[str, dict[str, Any]]) -> dict[str, ThingPropertyBase]:
        """Parse ECP API Thing properties into ThingProperties objects.

        :param properties: dict of ECP API Thing properties dict.
        :return: dict of ThingProperty with the property ids as dict keys.
        """

        return {property_id: thing_property_from_ecp_dict(property_id, edge_property_dict) for
                property_id, edge_property_dict in properties.items()}

    @staticmethod
    def _parse_edge_api_actions(actions: dict[str, dict[str, Any]]) -> dict[str, ThingAction]:
        """Parse ECP API Thing actions into ThingAction objects.

        :param actions: dict of ECP API Thing actions dict.
        :return: dict of ThingAction with the actions keys as dict keys.
        """

        return {action_key: ThingAction.from_ecp_dict(action_key, edge_action_dict) for
                action_key, edge_action_dict in actions.items()}

    @staticmethod
    def _parse_edge_api_events(events: dict[str, dict[str, Any]]) -> dict[str, ThingEvent]:
        """Parse ECP API Thing events into ThingEvent objects.

        :param events: dict of ECP API Thing events dict.
        :return: dict of ThingEvent with the event keys as dict keys.
        """

        return {event_key: ThingEvent.from_ecp_dict(event_key, edge_event_dict) for
                event_key, edge_event_dict in events.items()}

    @classmethod
    def _parse_ecp_dict(cls, ecp_thing_dict: dict[str, Any]) -> dict[str, Any]:
        """Parse the ecp_thing_dict into the correct names and forms.

        :param ecp_thing_dict: The dict that contains all the Thing schema.
        :return: The same dict with names and forms updated.
        """

        del ecp_thing_dict['@type']
        if 'links' in ecp_thing_dict:
            ecp_thing_dict['links'] = cls._parse_edge_api_links(ecp_thing_dict['links'])
        if 'modified' in ecp_thing_dict:
            ecp_thing_dict['modified'] = datetime.strptime(ecp_thing_dict['modified'],
                                                           cls.EDGE_DATETIME_FORMAT)
        if 'properties' in ecp_thing_dict:
            ecp_thing_dict['properties'] = cls._parse_edge_api_properties(ecp_thing_dict['properties'])
        if 'actions' in ecp_thing_dict:
            ecp_thing_dict['actions'] = cls._parse_edge_api_actions(ecp_thing_dict['actions'])
        if 'events' in ecp_thing_dict:
            ecp_thing_dict['events'] = cls._parse_edge_api_events(ecp_thing_dict['events'])

        return ecp_thing_dict

    @classmethod
    def from_ecp_dict(cls, ecp_thing_dict: dict[str, Any],
                      properties: Optional[dict[str, Any]] = None) -> Thing:
        """Convert the dict from the ECP API into the class.

        :param ecp_thing_dict: Thing dict from the ECP API key.
        :param properties: Properties values as a dict with properties id as keys.
        :return: Thing object with the data from the ecp_thing_dict and properties.
        """

        ecp_thing_dict = cls._parse_ecp_dict(ecp_thing_dict)
        return cls(**ecp_thing_dict) if properties is None else cls(**{**ecp_thing_dict, **properties})

    @classmethod
    def updatable_property(cls, property_id: str) -> bool:
        """Check if the property isn't blocked."""

        return property_id not in cls._BLOCKED_EDGE_PROPERTIES

    # pylint: disable=unused-argument
    def __init__(self,
                 collection: str, title: str, description: str = "",
                 *,
                 space: str = '',
                 uid: Optional[str] = None,
                 thing_id: Optional[str] = None,
                 base: Union[ParseResult, str] = None, href: Optional[str] = None,
                 thing_models: Optional[dict[str, Any]] = None,
                 created: Optional[Union[str, datetime]] = None, modified: Optional[Union[str, datetime]] = None,
                 properties: Optional[dict[str, ThingPropertyBase]] = None,
                 actions: Optional[dict[str, ThingAction]] = None,
                 events: Optional[dict[str, Any]] = None,
                 **kwargs) -> NoReturn:
        """
        :param collection: Thing collection.
        :param title: Thing title.
        :param description: Thing description.
        :param space: Thing space in Altair Smartworks IoT.
        :param thing_id: Thing id.
        :param uid: Thing uid.
        :param base: Thing base url.
        :param href: Thing href.
        :param thing_models: Thing model names that was used to create the Thing schema.
        :param created: Datetime of the Thing creation.
        :param modified: Datetime of the Thing the latest schema update.
        :param properties: Thing properties.
        :param actions: Thing actions.
        :param events: Thing events.
        :param kwargs: Just to avoid exception when extra parameters are passed.
        """

        if isinstance(created, str):
            created = datetime.strptime(created, self.EDGE_DATETIME_FORMAT)
        if isinstance(modified, str):
            modified = datetime.strptime(modified, self.EDGE_DATETIME_FORMAT)

        self._thing_types = [Thing.__name__]
        self.title = title
        self.description = description
        self._space = space
        self.collection = collection

        self._uid = uid
        self._thing_id = thing_id
        self.base = base
        self._href = href

        self.thing_models = thing_models if thing_models is not None else {}

        self._created = created if created is not None else datetime.now()
        self._modified = modified if modified is not None else self._created

        self.properties = properties if properties is not None else self.default_properties()
        self.actions = actions if actions is not None else self.default_actions()
        self.events = events if events is not None else self.default_events()

        self.telemetry: Optional[Telemetry] = None

        self._thing_status = 'offline'

        self._function_callbacks: dict[Callable[[], NoReturn], Handle] = {}

    @property
    def thing_types(self):
        """A tuple with all the types that the Thing has.

        A tuple with all the types that the Thing has. This represents all the class that the Thing
        has and by default is only Thing. Update the internal attributes if inherit from this class."""

        return self._thing_types

    @property
    def space(self) -> str:
        """Thing space in Altair SmartWorks IoT"""

        return self._space

    @property
    def thing_id(self) -> str:
        """Thing uid"""

        return self._thing_id

    @property
    def uid(self) -> str:
        """Thing uid"""

        return self._uid

    @property
    def href(self) -> str:
        """Thing href"""

        return self._href

    @property
    def created(self) -> datetime:
        """Datetime when the Thing was created."""

        return self._created

    @property
    def modified(self) -> datetime:
        """Datetime of the last schema update. Not include the properties values."""

        return self._modified

    @property
    def thing_status(self) -> str:
        """Thing status."""

        return self._thing_status

    @property
    def property_names(self) -> list[str]:
        """List of all properties that the Thing has."""

        return list(self.properties.keys())

    def __eq__(self, other):
        return self._uid == other.uid

    def __hash__(self):
        return hash(self._uid)

    def __str__(self) -> str:
        return str(self.to_ecp_dict(include_all=True))

    def to_ecp_dict(self, *, include_all: bool = False) -> dict[str, Any]:
        """Convert the object to a dict that the ECP understand.

        :param include_all: If True, include all the empty attributes.
        :return: The dict that represent the object.
        """

        edge_api_thing_dict = {
            'title': self.title,
            'description': self.description,
            'collection': self.collection,
            'created': self._created.strftime(self.EDGE_DATETIME_FORMAT),
            'modified': self._modified.strftime(self.EDGE_DATETIME_FORMAT),
            'properties': {property_id: property_.to_ecp_dict() for property_id, property_ in
                           self.properties.items()},
            'actions': {action_key: action.to_ecp_dict() for action_key, action in self.actions.items()},
            'events': {event_key: event.to_ecp_dict() for event_key, event in self.events.items()},
        }

        if self._space or include_all:
            edge_api_thing_dict['space'] = self._space
        if self._uid or include_all:
            edge_api_thing_dict['uid'] = self._uid
        if self._thing_id or include_all:
            edge_api_thing_dict['id'] = self._thing_id
        if self.thing_types or include_all:
            edge_api_thing_dict['@type'] = self.thing_types
        if self.base or include_all:
            edge_api_thing_dict['base'] = self.space
        if self._href or include_all:
            edge_api_thing_dict['href'] = self._href

        return edge_api_thing_dict

    def on(self, telemetry: Optional[Telemetry] = None) -> NoReturn:  # pylint: disable=invalid-name
        """Turn on the thing. Set the thing status to online

        :param telemetry: Telemetry object to use for send telemetry data.
        """
        self._thing_status = 'online'
        if telemetry is not None:
            self.telemetry = telemetry

    def off(self) -> NoReturn:
        """Turn off the thing. Set the thing status to offline"""

        self._thing_status = 'offline'

    def has_property(self, property_id: str) -> bool:
        """Check if the object has the property_id."""

        return property_id in self.properties and hasattr(self, property_id)

    async def on_update(self, ecp_thing_dict: dict[str, Any]) -> NoReturn:
        """Method to update the Thing schema.

        Method to update the Thing schema. It checks if the key is not blocked, check if
        the object has the attributes and set the new value only if it is different. Before
        update the schema, it parses the dict.
        :param ecp_thing_dict: Dict from ECP API that contains the new Thing schema.
        """

        for key, value in self._parse_ecp_dict(ecp_thing_dict).items():
            key = self._PARSE_EDGE_KEYS[key] if key in self._PARSE_EDGE_KEYS else key
            if hasattr(self, key) and key not in self._BLOCKED_EDGE_KEYS and getattr(self, key) != value:
                setattr(self, key, value)  # Only change if it is different to avoid send it to edge

    async def on_set_property(self, property_id: str, property_value: Any) -> NoReturn:
        """Callback method for driver set property.

        Callback method for driver set property. This function check if the property_id is listed
        in the properties attributes and check if the action has an attributes with the same name.
        Also check if the property isn't blocked for external updates. In that case, send a error
        message to the Error event and send the last value of the property to the Edge only if the
        telemetry attribute is set.
        :param property_id: Property id.
        :param property_value: Property new value.
        """

        property_id = self._PARSE_EDGE_PROPERTIES if property_id in self._PARSE_EDGE_PROPERTIES else property_id
        if not self.has_property(property_id):
            logger.error("Property {}} not found in {} ({})", property_id, self.title, self.uid)
            await self.send_error(f"Property {property_id} not found")
        else:
            if self.updatable_property(property_id):
                try:
                    logger.debug("Updating property {} in {} ({}): {}", property_id, self.title, self.uid,
                                 str(property_value))
                    setattr(self, property_id, property_value)
                except Exception as exception:  # pylint: disable=broad-except
                    logger.error(exception)
                    await self.send_error(exception)
            else:
                logger.debug("Property {} is blocked in {} ({}) for extern updates. Only read", property_id, self.title,
                             self.uid)
                await self.send_error(f"Property {property_id} is blocked for extern updates. Only read")
                await self.send_properties(property_ids=(property_id,))

    async def on_request_action(self, action_key: str, action_id: str, input_: Optional[Any] = None) -> NoReturn:
        # pylint: disable=too-many-branches
        """Callback function for a driver request action.

        Callback function for a driver request action. This method check if the action key is listed
        in the actions attributes and the object has a method with the same name. If this is valid,
        execute the method (Use await if the function is an async one). The method pass the parameters
        directly if the action is one single parameter, pass as a list if it is an array and pass it
        as a dict if the action require an object properties. For that, it uses the action input attribute.
        Also send the action status to the Edge if the telemetry attribute is set and also send the errors
        if it occurs.
        :param action_key: Action key.
        :param action_id: Action request id.
        :param input_: Action input parameters.
        """

        await self.telemetry.publish_action_status(self.uid, action_key, action_id, ActionRequestStatus.RECEIVED)

        if action_key not in self.actions or not hasattr(self, action_key):
            logger.warning("Action {} not found in {} ({})", action_key, self.title, self.uid)
            await self.send_error(f"Action {action_key} not found")
            return

        action: ThingAction = self.actions[action_key]
        action_function = getattr(self, action_key)
        action_status = ActionRequestStatus.COMPLETED
        try:
            if asyncio.iscoroutinefunction(action_function):
                if input_ is None:
                    res = await action_function()
                else:
                    if action.input is None:
                        res = await action_function()
                    elif isinstance(action.input, ThingPropertyArray):
                        res = await action_function(*input_)
                    elif isinstance(action.input, ThingPropertyObject):
                        res = await action_function(**input_)
                    else:
                        res = await action_function(input_)
            else:
                if input_ is None:
                    res = action_function()
                else:
                    if action.input is None:
                        res = action_function()
                    elif isinstance(action.input, ThingPropertyArray):
                        res = action_function(*input_)
                    elif isinstance(action.input, ThingPropertyObject):
                        res = action_function(**input_)
                    else:
                        res = action_function(input_)
            if res is not None and action_key in self.events:
                await self.telemetry.publish_event(self.uid, action_key, res)
        except Exception as exception:  # pylint: disable=broad-except
            action_status = ActionRequestStatus.ERROR
            logger.error(exception)
            await self.send_error(exception)
        finally:
            await self.telemetry.publish_action_status(self.uid, action_key, action_id, action_status)

    def edge_properties_dict(self, property_ids: Optional[Iterable[str]] = None) -> dict[str, Any]:
        """Return a dict with all the properties as keys and its values.

        :param property_ids: If present, only return the properties and values listed.
        :return: A dict with properties as keys and its values.
        """

        if not property_ids:
            property_ids = self.properties.keys()
        return {property_id: getattr(self, property_id) for property_id in property_ids if hasattr(self, property_id)}

    def set_callback_function(self, function: Callable[[], NoReturn],
                              time_interval: float, auto_run: bool = True) -> NoReturn:
        """Execute the function/method passed in a separate thread inside the object every time_interval seconds.

        :param function: The function or method to execute.
        :param time_interval: The time interval between calls.
        :param auto_run: If True, run the thread if it isn't running.
        """

        if time_interval <= 0.0:
            raise ValueError("time_interval must be positive")
        if auto_run and not self.is_running():
            self.run()
        self._function_callbacks[function] = self._callback_function_loop.call_soon_threadsafe(
            functools.partial(self._callback_function, function, time_interval))

    def unset_callback_function(self, function: Callable[[], NoReturn]) -> NoReturn:
        """Stop the function which it is schedule to run using set_callback_function method.

        :param function: Function to stop from the schedule.
        """

        if function in self._function_callbacks:
            self._function_callbacks[function].cancel()

    def _callback_function(self, function: Callable[[], NoReturn], time_interval: float) -> NoReturn:
        """Method to run the function every time_interval seconds in the proper way.

        :param function: The function or method to execute.
        :param time_interval: The time interval between calls.
        """

        if asyncio.iscoroutinefunction(function):  # Check if the function is async and run it on asyncio loop.
            self._callback_function_loop.create_task(function())
        else:
            function()

        # Schedule the function with call_later asyncio loop method.
        self._function_callbacks[function] = self._callback_function_loop.call_later(time_interval,
                                                                                     functools.partial(
                                                                                         self._callback_function,
                                                                                         function, time_interval))

    def schedule_send_properties(self, time_interval: float) -> NoReturn:
        """Execute send properties method every time_interval in a separate thread.

        :param time_interval: Indicates the time interval between method calls.
        """

        self.set_callback_function(self.send_properties, time_interval)

    async def send_properties(self, property_ids: Optional[Iterable[str]] = None) -> NoReturn:
        """Send the properties values to the Telemetry.

        Send all the properties available as an object attribute and listed in the properties'
        dict attribute. If property_ids is passed, only send these properties.
        :param property_ids: Is present, only send these properties. It must be an iterable
        of property ids and must be listed in the properties' dict attributes and as an object
        attributes.
        """

        if self.telemetry is not None and not self.telemetry.is_closed():
            await self.telemetry.publish_properties(self.uid, self.edge_properties_dict(property_ids))

    async def send_error(self, error: Union[str, Exception]) -> NoReturn:
        """Send an error message to the Error event.

        :param error: The error message to send.
        """

        if isinstance(error, Exception):
            error = str(error)
        if self.telemetry is not None and not self.telemetry.is_closed() and 'errors' in self.events:
            await self.telemetry.publish_event(self.uid, 'errors', error)

    async def send_warning(self, warning: str) -> NoReturn:
        """Send a warning message to the Warning event.

        :param warning: The warning message to send.
        """

        if self.telemetry is not None and not self.telemetry.is_closed() and 'errors' in self.events:
            await self.telemetry.publish_event(self.uid, 'warnings', warning)

    async def send_info(self, info: str) -> NoReturn:
        """Send an info message to the Info event.

        :param info: The info message to send.
        """

        if self.telemetry is not None and not self.telemetry.is_closed() and 'errors' in self.events:
            await self.telemetry.publish_event(self.uid, 'info', info)
