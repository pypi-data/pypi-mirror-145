"""Altair Smartworks Edge Compute Platform request action.

This script contains the class that represents an Altair Smartworks Edge Compute
Platform action event. The action is function that can be call for a certain Thing
and this is the representation of this request like turn_light_on and contains the
data send and the status as well as the datatime when it was requested and completed.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ActionRequestStatus(str, Enum):
    """Enum to specify the ActionRequest status"""

    PENDING = 'pending'
    RECEIVED = 'received'
    COMPLETED = 'completed'
    ERROR = 'error'


class ActionRequest(BaseModel):
    """Represent the status of a request of a Thing action

    :var key: Action key.
    :var uid: Action ID.
    :var thing_id: Thing ID which has the action key.
    :var href: Href of the execution.
    :var status: Status of the action request.
    :var action_input: The input data that sent to the action at the request execution.
    :var requested: Datetime when the action was requested in '%Y-%m-%dT%H:%M:%SZ' format.
    :var completed: Datetime when the action was completed or None if not completed in
    '%Y-%m-%dT%H:%M:%SZ' format.
    """

    key: str
    uid: str
    thing_id: str
    href: str
    status: ActionRequestStatus
    action_input: Any
    requested: datetime = Field(..., alias='timeRequested')
    completed: Optional[datetime] = Field(None, alias='timeCompleted')

    @classmethod
    def _parse_ecp_dict(cls, ecp_action_request_dict: dict[str, Any]) -> dict[str, Any]:
        """Parse the dict returned by the ECP API into correct keys and values for the class.

        :param ecp_action_request_dict: Dict from ECP API.
        :return: The dict with correct keys and values for the class.
        """

        href = ecp_action_request_dict['href'].split('/')
        ecp_action_request_dict['uid'] = href[-1]
        ecp_action_request_dict['thing_id'] = href[2]
        return ecp_action_request_dict

    @classmethod
    def from_ecp_dict(cls, key: str, ecp_action_request_dict: dict[str, Any]) -> ActionRequest:
        """Convert the dict from the ECP API into the class.

        :param key: Action key.
        :param ecp_action_request_dict: Action dict from the ECP API.
        :return: ActionRequest object with the data from the edge_api_action_request_response_dict.
        """

        ecp_action_request_dict = cls._parse_ecp_dict(ecp_action_request_dict)
        return cls(key=key, **ecp_action_request_dict)

    def is_completed(self) -> bool:
        """Check if the action is completed

        :return: True if the action is completed and False in other case.
        """

        return self.completed is not None

    def __eq__(self, other: Any):
        if not isinstance(other, ActionRequest):
            return False
        return self.href == other.href

    def __hash__(self):
        return hash(self.href)

    class Config:
        allow_mutation = False
