__all__ = [
    'clang_tidy',
    'gcc4',
    'clang',
    'msvc'
]

from abc import ABC
from typing import List

from sap.issue import Issue


class IssueParser(ABC):
    pattern: str

    def parse(self, content: str) -> List[Issue]:
        raise NotImplementedError()
