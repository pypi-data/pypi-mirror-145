"""The base class and utilities for templateable objects."""
from typing import Any

# Global NoValue can be used to omit a value
# (because a function that does not return any value returns None)
# To check, you can use `foo is NoValue`
NoValue = object()


class Templatable:
    """An object that is able to be converted into a template."""

    def generate(self) -> str:
        """generate generates a template from the Templatable."""
        raise NotImplementedError("generate() must be implemented")

    def propval(self, k: str) -> Any:
        """propval retrieves the property value for the given key."""
        try:
            val = getattr(self, k)
        except AttributeError:
            val = NoValue

        if val is NoValue:
            return val

        if callable(val):
            return val()

        return val
