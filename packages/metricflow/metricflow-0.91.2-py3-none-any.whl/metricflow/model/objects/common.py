from __future__ import annotations

from typing import Optional

from metricflow.model.objects.utils import HashableBaseModel
from metricflow.object_utils import ExtendedEnum
from metricflow.specs import LinkableElementReference


class Version(HashableBaseModel):  # noqa: D
    major: int
    minor: int

    @staticmethod
    def parse(version: str) -> Version:  # noqa: D
        if version[0] == "v":
            version = version[1:]

        parts = version.split(".")
        if len(parts) != 2:
            raise RuntimeError(f"Invalid version string in configs: {version}")

        return Version(major=int(parts[0]), minor=int(parts[1]))


class Element:  # noqa: D
    name: LinkableElementReference
    expr: Optional[str]
    type: ExtendedEnum

    @property
    def is_primary_time(self) -> bool:  # noqa: D
        raise NotImplementedError(
            f"Subclasses of Element must implement `is_primary_time`. This object is of type {type(self)}"
        )


class SourceFile(HashableBaseModel):  # noqa: D
    path: str
    contents: str


class Commit(HashableBaseModel):  # noqa: D
    commit: str
    timestamp: int


class FileSlice(HashableBaseModel):  # noqa: D
    filename: str
    content: str
    start_line_number: int
    end_line_number: int


class YamlConfigFile(HashableBaseModel):  # noqa: D
    filepath: str
    contents: str
    url: str


class SourceContext(HashableBaseModel):  # noqa: D
    definition_hash: str
