"""AMQP connection variables for Altair Smartworks Edge Compute Platform.

This script allow getting from environmental variable the variables to connect to
Edge Compute Platform RabbitMQ. This is usefully when the app is running in a
docker alongside ECP APP
"""

import os


def amqp_protocol() -> str:
    """Get the Edge Compute Platform AMQP protocol using AMQP_PROTOCOL environment variable."""
    return os.environ['AMQP_PROTOCOL']


def amqp_host() -> str:
    """Get the Edge Compute Platform AMQP host using AMQP_HOST environment variable."""
    return os.environ['AMQP_HOST']


def amqp_port() -> int:
    """Get the Edge Compute Platform AMQP port using AMQP_PORT environment variable."""
    return int(os.environ['AMQP_PORT'])
