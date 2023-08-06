
__all__ = ('APIException',)


class APIException(Exception):
    """
    An error occurred while processing an API the request.
    """

    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message
