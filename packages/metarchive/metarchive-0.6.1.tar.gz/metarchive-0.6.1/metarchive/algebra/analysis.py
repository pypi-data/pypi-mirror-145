from typing import Callable, TypeAlias, Iterable, TypeVar, Protocol, Optional, ParamSpec
from datetime import datetime
from json import dumps
from requests import get
from metarchive.algebra.types import ArchiveLink, find_links


class TagType(Protocol):
    """
    Protocol used for all analysers. A tag represents a html element within a html document.
    """
    name: str
    """
    Name of the tag.
    """
    attrs: dict[str, str | list [str]]
    """
    Attributes of the tag.
    """

AnalysisOptions = ParamSpec('AnalysisOptions')
DocumentType: TypeVar = TypeVar('DocumentType')
TagPredicate: TypeAlias = Callable[[str | TagType], bool]
"""
Callable taking a tag name or a tag and deciding if the tag should be searched for archive.org links.
"""

AllTags: TagPredicate = lambda _: True


class AnalyseDocument(Protocol):
    """
    Takes the content of a html file and an optional tag predicate to search the specified content for archive.org links.
    """
    def __call__(self, content: bytes, tag_predicate: TagPredicate = AllTags) -> Iterable[ArchiveLink]: ...


class AnalyseURL(Protocol):
    """
    Takes an url and an optional tag predicate to search the url's content for archive.org links.
    """

    def __call__(self, url: str, tag_predicate: TagPredicate = AllTags) -> Iterable[ArchiveLink]: ...


def create_document_analyser(
    parse_document: Callable[[bytes], DocumentType],
    get_elements: Callable[[DocumentType, TagPredicate], Iterable[TagType]],
) -> AnalyseDocument:
    def analyse(content: bytes, tag_predicate: TagPredicate = lambda _: True) -> Iterable[ArchiveLink]:
        for tag in get_elements(parse_document(content), tag_predicate):
            for attribute in tag.attrs.values():
                for link in find_links(attribute):
                    yield link

    return analyse


def create_url_analyser(
        parse_document: Callable[[bytes], DocumentType],
        get_elements: Callable[[DocumentType, TagPredicate], Iterable[TagType]],
) -> AnalyseURL:

    def analyse(url: str, tag_predicate: TagPredicate = lambda _: True) -> Iterable[ArchiveLink]:
        with get(url) as response:
            for tag in get_elements(parse_document(response.content), tag_predicate):
                for attribute in tag.attrs.values():
                    for link in find_links(attribute):
                        yield link

    return analyse


class DownloadError(ConnectionError):
    def __init__(self, url: str, status_code: int, link: ArchiveLink):
        super().__init__(f'{url}: HTTP {status_code}')
        self.status_code: int = status_code
        self.url: str = url
        self.archive_link: ArchiveLink = link

    @property
    def encoded(self) -> dict[str, str | int | datetime]:
        return dict(error='DownloadError', status_code=self.status_code, url=self.url, link=self.archive_link.dict())


def download(link: ArchiveLink) -> bytes:
    """
    Attempts to download an archive url.
    Args:
        link: Archive link to download
    Returns:
        Binary content of the target url
    Raises:
         DownloadError in case of an unsuccessful status code (not equal to 200)
    """
    with get(link.url) as response:
        if response.status_code != 200:
            raise DownloadError(response.url, response.status_code, link)
        else:
            return response.content
