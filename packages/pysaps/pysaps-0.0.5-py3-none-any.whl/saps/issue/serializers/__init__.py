import json
from abc import ABC
from pathlib import Path
from typing import List

from saps.issue import Issue


class Serializer(ABC):

    @classmethod
    def serialize(cls, issues: List[Issue]) -> List[dict]:
        return issues

    @classmethod
    def serialize_to_file(cls, issues: List[Issue], filename: Path, append=False):
        issues_serialized = cls.serialize(issues)
        if append and filename.is_file():
            issues_serialized.extend(json.load(open(filename, 'r')))
        json.dump(issues_serialized, open(filename, 'w'))


__all__ = [
    'Serializer',
    'gitlab'
]
