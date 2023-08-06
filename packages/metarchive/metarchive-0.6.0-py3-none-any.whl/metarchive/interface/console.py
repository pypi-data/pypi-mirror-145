from typing import Callable, Any
from json import dumps
from argparse import ArgumentParser
from multiprocessing.pool import ThreadPool
from datetime import date, datetime, timedelta
from metarchive.algebra.types import parse_link, ArchiveLink, ArchivePage
from metarchive.algebra.acquisition import and_, or_, only_domains, is_special_category, links_between, walk
from metarchive.algebra.log import write_to_log
from metarchive.aquicision.basic import create_basic_acquisition, DownloadError, AcquisitionError
from metarchive.aquicision.progress import create_acquisition_monitor



def main():
    last_two_weeks: timedelta = timedelta(days=14)

    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('initial_url', metavar='INITIAL_URL')
    parser.add_argument('--domains', action='append', default=[], help='Domains to allow for acquisition.')
    parser.add_argument('--external-files', type=bool, help='Acquire external files, even if from another domain.')
    parser.add_argument('--start', type=int, default=0, help='Lower archive date limit.')
    parser.add_argument('--to', type=int, default=0, help='Upper archive date limit.')
    parser.add_argument('--threads', type=int, default=10, help='Number of threads to use.')
    parser.add_argument('--out')
    args = parser.parse_args()

    initial_link: ArchiveLink = parse_link(args.initial_url)
    domains: set[str] = {initial_link.original_url.host}.union(set(args.domains))
    start: datetime | None = (initial_link.timestamp - timedelta(days=args.start)) if args.start else None
    end: datetime = initial_link.timestamp + timedelta(days=args.to)
    predicate: Callable[[ArchiveLink], bool] = and_(only_domains(domains), links_between(start, end))
    out: str = args.out if args.out else f'{initial_link.original_url.host}_{initial_link.timestamp.isoformat()}.jl'
    if args.external_files:
        predicate = or_(predicate, is_special_category)
    print(
        f"Starting acquisition of {initial_link.original_url} from {start.isoformat() if start else 'any'} to {end.isoformat()}"
    )

    with open(out, 'a+', encoding='utf-8') as log:
        with ThreadPool(args.threads) as pool:
            for result in walk(
                create_basic_acquisition(),
                [initial_link],
                predicate,
                pool.imap_unordered,
                callback=create_acquisition_monitor()
            ):
                write_to_log(result, log)


if __name__ == '__main__':
    main()