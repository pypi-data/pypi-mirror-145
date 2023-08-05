from functools import wraps
from inspect import signature

from ..exceptions import StorageClientException


def validate_encryption_enabled(function):
    @wraps(function)
    def inner(*args, **kwargs):
        class_instance = args[0] if "self" in signature(function).parameters else None
        if class_instance and not class_instance.encrypt:
            raise StorageClientException(
                f"Validation failed during {function.__qualname__}(): "
                f"This method is only allowed with encryption enabled"
            )
        return function(*args, **kwargs)

    return inner
