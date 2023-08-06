from dataclasses import dataclass
from typing import Optional

from sap.issue.severity import Severity


@dataclass()
class Issue:
    id: Optional[str] = None
    path: Optional[str] = None
    filename: Optional[str] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    column_start: Optional[int] = None
    column_end: Optional[int] = None
    category: Optional[str] = None
    type: Optional[str] = None
    package: Optional[str] = None
    module: Optional[str] = None
    severity: Severity = None
    message: Optional[str] = None
    description: Optional[str] = None
    origin: Optional[str] = None
    origin_name: Optional[str] = None
    reference: Optional[str] = None
    fingerprint: Optional[str] = None
    properties: Optional[str] = None

    def __post_init__(self):
        if self.line_end is None and self.line_start is not None:
            self.line_end = self.line_start
        if self.column_end is None and self.column_start is not None:
            self.column_end = self.column_start
