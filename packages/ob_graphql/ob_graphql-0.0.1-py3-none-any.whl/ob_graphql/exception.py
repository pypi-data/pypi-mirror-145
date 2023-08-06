class ConnectionException(Exception):
    """Exception thrown during connection errors to the GraphQL server"""


class InvalidPayloadException(Exception):
    """Exception thrown if payload recived from server is mal-formed or cannot be parsed"""
