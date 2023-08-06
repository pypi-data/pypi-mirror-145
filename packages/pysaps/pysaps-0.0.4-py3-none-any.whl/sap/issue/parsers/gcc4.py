import re
from typing import List

from sap.issue import Issue
from sap.issue.parsers import IssueParser
from sap.issue.severity import Severity


class GCC4(IssueParser):
    GCC_WARNING_PATTERN = r"^(?:.*\[[^]]*\])?\s*(.+?):(\d+):(?:(\d+):)? ?([wW]arning|.*[Ee]rror): (.*)$"
    CLASS_PATTERN = r"\[-W(.+)]$"

    @classmethod
    def is_line_interesting(cls, line: str) -> bool:
        return 'arning' in line or 'rror' in line

    @classmethod
    def is_message_continuation(cls, line: str) -> bool:
        if len(line) < 3:
            return False
        if line[0] in ('/', '[', '<', '='):
            return False
        if line[1] == ':':
            return False
        if line[2] == '/' or line[0] == '\\':
            return False
        return not any([c in line.lower() for c in ('arning', 'rror', 'make')])

    @classmethod
    def parse(cls, content: str) -> List[Issue]:
        issues = []
        # lines = [l for l in content.splitlines() if len(l) > 0]
        lines = content.splitlines()

        line_idx = 0
        while line_idx < len(lines):
            line = lines[line_idx]
            match = re.match(cls.GCC_WARNING_PATTERN, line)
            if match is None:
                line_idx += 1
                continue
            g0, g1, g2, g3, g4, g5 = (match.group(i) for i in range(6))
            message = g5.lstrip() if g5 else ''

            klass_match = re.search(cls.CLASS_PATTERN, line)
            category = None
            if klass_match is not None and klass_match.group(1):
                category = klass_match.group(1)

            cnt = 1
            found_related_issues = False
            while line_idx + cnt < len(lines) and cls.is_message_continuation(lines[line_idx + cnt]):
                found_related_issues = True
                message = f'{message}\n{lines[line_idx + cnt]}'
                cnt += 1
                issues.append(Issue(filename=g1,
                                    category=category,
                                    line_start=g2,
                                    column_start=g3,
                                    message=message,
                                    severity=Severity.guess_from_string(g4)))

            if found_related_issues:
                line_idx = line_idx + cnt
                continue
            else:
                line_idx += 1
            issues.append(Issue(filename=g1,
                                category=category,
                                line_start=g2,
                                column_start=g3,
                                message=message,
                                severity=Severity.guess_from_string(g4)))

        return issues
