from typing import Any
from argparse import ArgumentParser
from sys import stderr
from json import loads, JSONDecodeError
from metarchive.algebra.types import ArchivePage


def main():
    parser: ArgumentParser = ArgumentParser('Print all acquired links.')
    parser.add_argument('target', metavar='TARGET')
    args = parser.parse_args()
    pages: list[ArchivePage] = list()
    with open(args.target, encoding='utf-8') as src:
        while True:
            line: str = src.readline()
            if not line:
                break
            try:
                entry: dict[str, Any] = loads(line)
                if 'error' not in entry:
                    pages.append(ArchivePage(**entry))
            except JSONDecodeError:
                print(
                    'Could not decode line, if the file is still actively appended to, this is expected behaviour.',
                    file=stderr
                )
    for page in pages:
        print(page.archive_link.original_url, '\t', page.archive_link.timestamp.isoformat())


if __name__ == '__main__':
    main()