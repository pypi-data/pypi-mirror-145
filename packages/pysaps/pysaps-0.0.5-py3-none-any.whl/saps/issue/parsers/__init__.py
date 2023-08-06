from abc import ABC
from typing import List

from saps.issue import Issue


class IssueParser(ABC):
    pattern: str

    @staticmethod
    def parse(cls, content: str) -> List[Issue]:
        raise NotImplementedError()


__all__ = [
    'clang_tidy',
    'gcc4',
    'clang',
    'msvc',
    'IssueParser'
]
