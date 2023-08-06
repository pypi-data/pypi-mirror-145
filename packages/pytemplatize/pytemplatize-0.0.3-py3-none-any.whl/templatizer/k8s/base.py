"""Base support code for Kubernetes template generation."""
from typing import Any, List

import yaml

from templatizer import NoValue, Templatable


def fix_value(val: Any):
    """fix_value fixes value types to embed into YAML correctly."""
    if isinstance(val, list):
        return [fix_value(v) for v in val]

    # Other templatable objects should be emitted correctly
    if isinstance(val, Templatable):
        val = yaml.load(val.generate(), Loader=yaml.Loader)

    return val


class K8STemplatable(Templatable):
    """K8STemplatable is the base class for all Kubernetes template objects."""

    description = NoValue
    apiVersion = NoValue
    kind = NoValue
    required_props: List[str] = []

    def generate(self) -> str:
        document = {}

        props = self.propval("props")
        required_props = self.propval("required_props")
        for prop in props:
            val = self.propval(prop)
            # K8S-specific feature: returning None also ignores the value
            if val is not NoValue and val:
                val = fix_value(val)
                document[prop] = val
            elif prop in required_props:
                raise ValueError(f'no value for required property "%{prop}s"')

        return yaml.dump(document)
