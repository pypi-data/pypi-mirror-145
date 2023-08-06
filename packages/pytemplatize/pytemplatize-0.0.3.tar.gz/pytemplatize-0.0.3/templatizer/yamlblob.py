"""Provides YAML 'blob' template classes for embedding YAML as strings."""
from typing import Any

import yaml

from .templatable import Templatable


def string_as_block(dumper, data):
    """string_as_block uses YAML's block style for strings with newlines."""
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, string_as_block)


class YamlBlob(Templatable):
    """YamlBlob embeds data as a YAML string."""

    def data(self) -> Any:
        """data returns the raw data to be YAML-encoded."""
        raise NotImplementedError("data() must be implemented on ConfigurationData")

    def generate(self) -> str:
        return yaml.dump(self.data())
