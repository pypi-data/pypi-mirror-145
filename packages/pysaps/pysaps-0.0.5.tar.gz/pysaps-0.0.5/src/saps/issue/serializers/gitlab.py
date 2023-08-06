import hashlib
import json
from typing import List

from saps.issue import Issue
from saps.issue.serializers import Serializer
from saps.issue.severity import Severity

severity_lut = {
    Severity.ERROR: 'blocker',
    Severity.WARNING_HIGH: 'critical',
    Severity.WARNING_NORMAL: 'major',
    Severity.WARNING_LOW: 'minor'
}


class Gitlab(Serializer):
    @classmethod
    def serialize(cls, issues: List[Issue]) -> List[dict]:
        ret = []
        for issue in issues:
            e = {
                'description': issue.message,
                'severity': severity_lut[issue.severity],
                'location': {
                    'path': issue.filename,
                    'lines': {}
                }
            }
            e['fingerprint'] = hashlib.md5(json.dumps(e).encode('utf-8')).hexdigest()
            e['location']['lines']['begin'] = issue.line_start
            ret.append(e)
        return ret
