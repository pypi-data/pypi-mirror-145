from enum import Enum


class Severity(Enum):
    ERROR = "ERROR"
    WARNING_HIGH = "WARNING_HIGH"
    WARNING_NORMAL = "WARNING_NORMAL"
    WARNING_LOW = "WARNING_LOW"

    @classmethod
    def guess_from_string(cls, severity: str) -> 'Severity':
        if any(ss in severity for ss in ("error", "severe", "critical", "fatal")):
            return Severity.ERROR
        if any(ss in severity for ss in ("info", "note")):
            return Severity.WARNING_LOW
        if any(ss in severity for ss in ("warning",)):
            return Severity.WARNING_NORMAL
        return Severity.WARNING_LOW

    def __str__(self):
        return self.value
