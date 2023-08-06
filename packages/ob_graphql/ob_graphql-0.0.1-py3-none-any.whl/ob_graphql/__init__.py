"""A simple GraphQL client that works over Websocket as the transport protocol, instead of HTTP."""

__version__ = "0.0.1"

from ob_graphql.client import OBQLClient as OBQLClient

__all__ = ["OBQLClient"]
