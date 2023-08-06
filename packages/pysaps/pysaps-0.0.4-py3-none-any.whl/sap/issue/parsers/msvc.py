import re
from typing import List

from sap.issue import Issue
from sap.issue.parsers import IssueParser
from sap.issue.severity import Severity


class MSVC(IssueParser):
    pattern = "^(?P<filename>.*)\((?P<line_start>\d+)\)\s*:\swarning\s(?P<category>C\d+):\s*(?P<message>.*)$"

    @classmethod
    def parse(cls, content: str) -> List[Issue]:
        issues = []
        for line in content.splitlines():
            try:
                match: dict = next(re.finditer(cls.pattern, line)).groupdict()
            except StopIteration:
                continue
            match['line_start'] = int(match['line_start'])
            match['severity'] = Severity.WARNING_NORMAL
            # match['column_start'] = 0
            issues.append(Issue(**match))
        return issues
