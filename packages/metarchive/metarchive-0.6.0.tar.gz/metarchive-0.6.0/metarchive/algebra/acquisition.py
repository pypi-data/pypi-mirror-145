from typing import Protocol, Iterable, Callable, TypeVar
from json import dumps
from operator import __and__, __or__
from toolz import comp, juxt, partial
from datetime import datetime
from metarchive.algebra.types import ArchiveLink, ArchivePage
from metarchive.algebra.analysis import AnalyseDocument, TagPredicate, AllTags, DownloadError


def all_links(_: ArchiveLink) -> bool: return True


def links_between(start: datetime | None, end: datetime | None) -> Callable[[ArchiveLink], bool]:
    if not start and not end:
        return all_links
    end = end if end else datetime.now()
    start = start if start else datetime(1970, 1, 1)

    def is_in_range(link: ArchiveLink) -> bool:
        return start <= link.timestamp <= end
    return is_in_range


def is_special_category(link: ArchiveLink) -> bool:
    return bool(link.category)


def only_domains(domains: set[str]) -> Callable[[ArchiveLink], bool]:
    def is_in_domain(link: ArchiveLink) -> bool:
        return any(map(link.original_url.host.endswith, domains))
    return is_in_domain


T = TypeVar('T')
D = TypeVar('D')


def _apply(func: Callable[[T, T], D], args: tuple[T, T]) -> Callable[[tuple[T, T]], D]:
    return func(*args)


def and_(first: Callable[[ArchiveLink], bool], second: Callable[[ArchiveLink], bool]) -> Callable[[ArchiveLink], bool]:
    return comp(partial(_apply, __and__), juxt(first, second))


def or_(first: Callable[[ArchiveLink], bool], second: Callable[[ArchiveLink], bool]) -> Callable[[ArchiveLink], bool]:
    return comp(partial(_apply, __or__), juxt(first, second))


class AcquisitionError(RuntimeError):
    def __init__(self, original_error: Exception, archive_link: ArchiveLink):
        super().__init__(str(original_error))
        self.original_error = original_error
        self.archive_link: ArchiveLink = archive_link

    @property
    def encoded(self) -> dict[str, str | datetime]:
        return dict(
                error='AcquisitionError', archive_link=self.archive_link.dict(),
                original_error_type=type(self.original_error).__name__, original_error_message=str(self.original_error)
            )


class AcquireLink(Protocol):
    def __call__(
        self,
        target: ArchiveLink
    ) -> Iterable[ArchivePage | ArchiveLink | DownloadError | AcquisitionError]:
        ...


CallbackArguments = ArchiveLink | ArchivePage | DownloadError | AcquisitionError
AcquisitionCallback = Callable[[CallbackArguments], None]


def walk(
    acquire_link: AcquireLink,
    targets: Iterable[ArchiveLink],
    link_predicate: Callable[[ArchiveLink], bool] = all_links,
    distribute_work: Callable[[AcquireLink, Iterable[ArchiveLink]], Iterable[Iterable[ArchiveLink]]] = map,
    already_visited: set[str] | None = None,
    callback: AcquisitionCallback | None = None
) -> Iterable[ArchivePage | DownloadError | AcquisitionError]:
    already_visited: set[str] = already_visited if already_visited else set()
    next_targets: set[ArchiveLink] = set(filter(link_predicate, targets))
    follow_up_links: set[ArchiveLink] = set(next_targets)

    while follow_up_links:
        next_targets = set(follow_up_links)
        follow_up_links.clear()
        results: Iterable[ArchivePage | ArchiveLink | DownloadError | AcquisitionError] = (
            result for results in distribute_work(acquire_link, next_targets) for result in results
        )
        for result in results:
            match result:
                case ArchivePage() as page:
                    yield page
                    already_visited.add(page.archive_link.original_url)
                    if callback:
                        callback(result)
                case ArchiveLink() as link:
                    if link.original_url not in already_visited and link_predicate(link):
                        follow_up_links.add(link)
                        if callback:
                            callback(link)
                case DownloadError() | AcquisitionError() as error:
                    yield error
                    if callback:
                        callback(error)

