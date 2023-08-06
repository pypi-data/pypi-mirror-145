"""Altair Smartworks Edge Compute Platform health services.

This script contains the class that represents an Altair Smartworks Edge Compute
Platform health services report. It contains the name and key of the services as
well as its status and same util datetimes.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class EdgeServiceHealthStatus(str, Enum):
    """Represent the different status of a service"""

    START = 'start'
    UP = 'up'
    SLEEP = 'sleep'
    DOWN = 'down'


class EdgeServiceHealth(BaseModel):
    """Represent the status and health of a service

    :var key: Service key.
    :var name: Service name.
    :var version: Service version deployed.
    :var status: Service health status.
    :var git_sha: Service build git SHA.
    :var built: Service build datetime in '%Y-%m-%dT%H:%M:%SZ' format.
    :var registered: Service registered datetime in '%Y-%m-%dT%H:%M:%SZ' format.
    :var updated: Service updated datetime in '%Y-%m-%dT%H:%M:%SZ' format.
    """

    key: str
    name: str
    namespace: str
    pods: list[str]
    version = str
    status: EdgeServiceHealthStatus
    git_sha: str = Field(..., alias="gitSha")
    built: datetime = Field(..., alias="buildDate")
    registered: datetime
    updated: datetime = Field(..., alias="lastUpdate")

    def __eq__(self, other: Any):
        if not isinstance(other, EdgeServiceHealth):
            return False
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    class Config:
        allow_mutation = False
