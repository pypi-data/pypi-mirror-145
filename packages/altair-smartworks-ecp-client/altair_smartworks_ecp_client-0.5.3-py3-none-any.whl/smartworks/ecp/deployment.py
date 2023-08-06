"""Kubernetes' variables for Altair Smartworks Edge Compute Platform.

This script allow getting from environmental variable the variables to get useful
information about the kubernetes deployment. This is usefully when the app is running
in a kubernetes alongside ECP APP
"""

import os


def node_name():
    """Get the kubernetes node name using MY_NODE_NAME environment variable."""

    return os.environ['MY_NODE_NAME']


def deployment_name():
    """Get the kubernetes deployment name using MY_DEPLOYMENT_NAME environment variable."""

    return os.environ['MY_DEPLOYMENT_NAME']


def pod_name():
    """Get the kubernetes pod name using MY_POD_NAME environment variable."""

    return os.environ['MY_POD_NAME']


def pod_namespace():
    """Get the kubernetes pod namespace using MY_POD_NAMESPACE environment variable."""

    return os.environ['MY_POD_NAMESPACE']


def pod_ip():
    """Get the kubernetes pod ip using MY_POD_IP environment variable."""

    return os.environ['MY_POD_IP']


def container_name():
    """Get the kubernetes container name using MY_CONTAINER_NAME environment variable."""

    return os.environ['MY_CONTAINER_NAME']
