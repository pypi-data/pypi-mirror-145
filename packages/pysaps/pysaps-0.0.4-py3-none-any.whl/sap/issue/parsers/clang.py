import re
from typing import List

from sap.issue import Issue
from sap.issue.parsers import IssueParser
from sap.issue.severity import Severity


class Clang(IssueParser):

    @classmethod
    def parse(cls, content: str) -> List[Issue]:
        pattern = r"^\s*(?:\d+%)?([^%]*?):(\d+):(?:(\d+):)?(?:(?:\{\d+:\d+-\d+:\d+\})+:)?\s*(warning|[^\[\]]*error):\s*(.*?)\s*(?:\[([^\[]*)\])?$"
        ignore_pattern = r"^-\[.*\].*$"
        issues = []

        for line in content.splitlines():
            match = re.match(pattern, line)
            if match is None:
                continue

            g0, g1, g2, g3, g4, g5, g6 = (match.group(i) for i in range(7))

            if re.search(ignore_pattern, g5):
                continue

            issues.append(Issue(filename=g1,
                                line_start=g2,
                                column_start=g3,
                                category=g6,
                                message=g5,
                                severity=Severity.WARNING_HIGH if 'error' in g4 else Severity.WARNING_NORMAL
                                ))
        return issues
