import argparse
import json
from pathlib import Path
from sys import stdin, stdout

from yaml import serialize

from saps.issue.parsers import *
from saps.issue.serializers import *

if __name__ == "__main__":
    parsers = IssueParser.__subclasses__()
    serializers = Serializer.__subclasses__()
    parser = argparse.ArgumentParser(description='Python Static Analysis Parsers.')
    parser.add_argument('--parser', choices=list(k.__name__ for k in parsers),
                        help='Specify a parser. If unspecified parser with most results will be used.')
    parser.add_argument('--input,-i', dest='input',
                        help='Specify input file to parse. If unspecified, input will be read from stdin')
    parser.add_argument('--output,-o', dest='output',
                        help='Specify output file to parse. If unspecified, output will be written to stdout')
    parser.add_argument('--serializer', choices=list(k.__name__ for k in serializers), help='Serialization format')
    args = parser.parse_args()

    if args.parser is not None:
        parsers = [p for p in parsers if p.__name__ == args.parser]
    assert len(parsers) > 0

    serializer = Serializer
    if args.serializer is not None:
        serializer = [s for s in serializers if s.__name__ == args.serializer][0]

    if args.input is not None:
        path = Path(args.input)
        assert path.is_file(), f"Couldn't find file \"{path}\""
        content = open(path).read()
    else:
        content = '\n'.join([line for line in stdin])

    issues = []
    for parser in parsers:
        _issues = parser().parse(content)
        if len(_issues) > len(issues):
            issues = _issues

    issues_serialized = serializer().serialize(issues)
    output = stdout
    if args.output is not None:
        output = open(args.output, 'w')
    json.dump(issues_serialized, output)
