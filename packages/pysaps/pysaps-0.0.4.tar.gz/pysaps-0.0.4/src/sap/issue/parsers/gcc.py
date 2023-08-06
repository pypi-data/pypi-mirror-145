import re
from typing import List
from xml.sax.saxutils import escape as xml_escape

from sap.issue import Issue
from sap.issue.parsers import IssueParser
from sap.issue.severity import Severity


class GCC(IssueParser):
    pattern = r"^(?:\s*(?:\[.*\]\s*)?([^ ]*\.[chpimxsola0-9]+):(?:(\d*):(?:\d*:)*\s*(?:(warning|error|note)\s*:|\s*(.*))|\s*(undefined reference to.*))(.*)|.*ld:\s*(.*-l(.*)))$"
    gcc_error = "GCC Error"
    linker_error = "Linker Error"

    @classmethod
    def parse(cls, content: str) -> List[Issue]:
        issues = []
        for line in content.splitlines():
            try:
                match = next(re.finditer(cls.pattern, line))
            except StopIteration:
                continue
            g0, g1, g2, g3, g4, g5, g6, g7, g8 = (match.group(i) for i in range(9))
            if g7 is not None:
                issues.append(Issue(filename=g8,
                                    line_start=0,
                                    category=cls.linker_error,
                                    message=g7,
                                    severity=Severity.WARNING_HIGH
                                    ))
                continue

            if "cleartool" in g1:
                continue

            if "foo.so" in line:
                print('here')

            if g3 is not None and "warning" == g3.lower():
                severity = Severity.WARNING_NORMAL
            elif g3 is not None and "error" == g3.lower():
                severity = Severity.WARNING_HIGH
            elif g3 is not None and "note" == g3.lower():
                severity = Severity.WARNING_LOW
            elif g4 is not None:
                if "instantiated from here" in g4.lower():
                    continue
                issues.append(Issue(filename=g1,
                                    line_start=int(g2),
                                    category=cls.gcc_error,
                                    message=xml_escape(g4),
                                    severity=Severity.WARNING_HIGH
                                    ))
                continue
            else:
                continue
                issues.append(Issue(filename=g1,
                                    line_start=0,
                                    category=cls.gcc_error,
                                    message=xml_escape(g5),
                                    severity=Severity.WARNING_HIGH))
                continue

            issues.append(Issue(filename=g1,
                                line_start=int(g2),
                                category=f"GCC {g3}",
                                message=xml_escape(g6),
                                severity=severity))

        return issues
