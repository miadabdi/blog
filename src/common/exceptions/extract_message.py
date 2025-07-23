"""
Helper to extract a message from an exception.
"""


def extract_message(exc: Exception) -> str:
    """
    Extracts the message from an exception, handling different types of exceptions.

    Args:
        exc (Exception): The exception from which to extract the message.

    Returns:
        str: The extracted message.
    """

    message = (
        getattr(exc, "detail", None)
        or getattr(exc, "message", None)
        or getattr(exc, "args", [None])[0]
        or str(exc)
        or "Unauthorized access"
    )

    return message
