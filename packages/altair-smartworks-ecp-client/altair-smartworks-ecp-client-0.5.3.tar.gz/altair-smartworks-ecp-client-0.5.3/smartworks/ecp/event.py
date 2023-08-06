"""Altair Smartworks Edge Compute Platform request event.

This script contains the class that represents an Altair Smartworks Edge Compute
Platform request event. The request event is data structure that save data like
logs, errors or events like is raining.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class EventRequest(BaseModel):
    """Represent q event of a Thing

    :var key: Event key.
    :var uid: Event ID.
    :var thing_id: Thing ID which has the event.
    :var href: href for the event request.
    :var data: data of the event.
    :var created: Datetime when the event is created in '%Y-%m-%dT%H:%M:%SZ' format.
    """

    key: str
    uid: str
    thing_id: str
    href: str
    data: Any
    created: datetime = Field(..., alias="timestamp")

    @classmethod
    def _parse_ecp_dict(cls, ecp_event_dict: dict[str, Any]) -> dict[str, Any]:
        """Parse the dict returned by the ECP API into correct keys and values for the class.

        :param ecp_event_dict: Dict from ECP API.
        :return: The dict with correct keys and values for the class.
        """
        href = ecp_event_dict['href'].split('/')
        ecp_event_dict['uid'] = href[-1]
        ecp_event_dict['thing_id'] = href[2]
        return ecp_event_dict

    @classmethod
    def from_ecp_dict(cls, key: str, ecp_event_dict: dict[str, Any]) -> EventRequest:
        """Convert the dict from the ECP API into the class.

        :param key: Event key.
        :param ecp_event_dict: Action dict from the ECP API.
        :return: ActionRequest object with the data from the edge_api_event_request_response_dict.
        """
        ecp_event_dict = cls._parse_ecp_dict(ecp_event_dict)
        return cls(key=key, **ecp_event_dict)

    def __eq__(self, other: Any):
        if not isinstance(other, EventRequest):
            return False
        return self.href == other.href

    def __hash__(self):
        return hash(self.href)
