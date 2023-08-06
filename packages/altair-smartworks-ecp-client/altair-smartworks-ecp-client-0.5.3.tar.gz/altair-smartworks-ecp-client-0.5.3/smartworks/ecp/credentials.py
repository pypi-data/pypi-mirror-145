"""Credential for Altair Smartworks Edge Compute Platform.

This file contains the functions that retinue the credential needed for
Altair Smartworks Edge Compute Platform from environmental variables. This
is usefully when the app is running in a docker alongside ECP APP
"""

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class EdgeCredentials:
    """ Altair Smartworks Edge Compute Platform credentials.

    Contains the username and password for the Altair Smartworks Edge Compute Platform
    and functions to retrieve it from environmental variables.
    """

    @staticmethod
    def api_user():
        """Get the API username using API_USER environmental variables

        :return: username for the API
        """

        return os.environ['API_USER']

    @staticmethod
    def api_password():
        """Get the API password using API_PASSWORD environmental variables

        :return: password for the API
        """

        return os.environ['API_PASSWORD']

    @classmethod
    def api_credentials(cls):
        """Get the API Credentials

        :return: Credentials for the API
        """

        return cls(cls.api_user(), cls.api_password())

    @staticmethod
    def device_driver_user():
        """Get the Driver username using DEVICE_DRIVER_USER environmental variables

        :return: username for the Driver
        """
        return os.environ['DEVICE_DRIVER_USER']

    @staticmethod
    def device_driver_password():
        """Get the Driver password using DEVICE_DRIVER_PASSWORD environmental variables

        :return: password for the Driver
        """
        return os.environ['DEVICE_DRIVER_PASSWORD']

    @classmethod
    def device_driver_credentials(cls):
        """Get the Driver Credentials

        :return: Credentials for the Driver
        """
        return cls(cls.device_driver_user(), cls.device_driver_password())

    @staticmethod
    def telemetry_user():
        """Get the Telemetry username using TELEMETRY_USER environmental variables

        :return: username for the Telemetry
        """
        return os.environ['TELEMETRY_USER']

    @staticmethod
    def telemetry_password():
        """Get the Telemetry password using TELEMETRY_PASSWORD environmental variables

        :return: password for the Telemetry
        """
        return os.environ['TELEMETRY_PASSWORD']

    @classmethod
    def telemetry_credentials(cls):
        """Get the Telemetry Credentials

        :return: Credentials for the Telemetry
        """
        return cls(cls.telemetry_user(), cls.telemetry_password())

    username: str = field(hash=True)
    password: str
