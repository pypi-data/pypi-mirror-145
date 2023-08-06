"""Altair Smartworks Edge Compute Platform label

This script contains the class that represents an Altair Smartworks Edge Compute
Platform Label.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, NoReturn, Optional

from pydantic import Field, BaseModel


class Label(BaseModel):
    """Class that represent a Thing Label

    :var name: Label name.
    :var uid: Label ID.
    :var val_regex: Optional regular expression that is used to validate the property value in telemetry data.
    :var conversion_opts: The conversion that will be applied.
    :var conversion_data: Represent the conversion between values in enum label. None if conversion_opts is not ConversionOption.ENUM
    """

    class ConversionOption(Enum):
        """Enum that represent the conversion options of a Label"""

        CELSIUS_TO_FAHRENHEIT = 'CELSIUS_TO_FAHRENHEIT'
        FAHRENHEIT_TO_CELSIUS = 'FAHRENHEIT_TO_CELSIUS'
        MULTIPLY_BY_1000 = 'MULTIPLY_BY_1000'
        DIVIDE_BY_1000 = 'DIVIDE_BY_1000'
        ENUM = 'ENUM'

    uid: str = Field(..., alias='labelId')
    name: str
    val_regex: str = Field(..., alias='validationRegex')
    conversion_opts: ConversionOption = Field(..., alias='conversionOption')
    conversion_data: Optional[str] = Field(None, alias='conversionData')

    def __eq__(self, other: Any):
        if not isinstance(other, Label):
            return False
        return self.uid == other.uid

    def __hash__(self):
        return hash(self.uid)

    def to_ecp_dict(self) -> dict[str, Any]:
        """Convert to Altair Smartworks ECP dict format."""

        return self.dict(include={'name', 'val_regex', 'conversion_opts', 'conversion_data'}, by_alias=True)

    def on_update(self, edge_api_label_dict: dict[str, Any]) -> NoReturn:
        """Call this method to update the attributes from a dict returned by the Edge.

        :param edge_api_label_dict: dict with the attributes. Equal attributes will be omitted.
        """
        for key, value in self.__class__(**edge_api_label_dict).items():
            if hasattr(self, key) and getattr(self, key) != value:
                setattr(self, key, value)  # Only change if it is different
