import re
from typing import List

from sap.issue import Issue
from sap.issue.parsers import IssueParser
from sap.issue.severity import Severity


class ClangTidy(IssueParser):
    pattern: str = r"((?P<filename>[^\s]+):(?P<line_start>\d+):(?P<column_start>\d+): |)(?P<severity>warning|error): (?P<message>.*?) \[(?P<category>[^\s]*?)\]$"

    @classmethod
    def parse(cls, content: str) -> List[Issue]:
        issues = []
        for line in content.splitlines():
            try:
                match: dict = next(re.finditer(cls.pattern, line)).groupdict()
            except StopIteration:
                continue
            for k in ('line_start', 'column_start'):
                if match[k] is None:
                    continue
                match[k] = int(match[k])
            match['type'] = match['severity'].capitalize()
            match['severity'] = Severity.ERROR if 'error' in match['severity'] else Severity.WARNING_NORMAL
            issues.append(Issue(**match))
        return issues
