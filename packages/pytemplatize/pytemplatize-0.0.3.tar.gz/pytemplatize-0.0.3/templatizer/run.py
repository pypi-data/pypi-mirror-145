"""Functions for running the generator."""
from typing import Iterable

from .templatable import Templatable


def run(objects: Iterable[Templatable], separator: str = "\n---\n"):
    """Run the generator on the given objects, adding a separator for each."""
    return separator.join(obj.generate() for obj in objects)
