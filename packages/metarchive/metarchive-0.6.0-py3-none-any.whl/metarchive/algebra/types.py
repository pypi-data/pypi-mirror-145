from datetime import datetime
from json import dumps
from base64 import b64encode
from itertools import chain
from typing import Generator
from re import compile, Pattern, Match
from pydantic import BaseModel, ValidationError, Field
from pydantic.networks import AnyUrl


_WAYBACK_URL_SCHEME: Pattern = compile(r'https?://web.archive.org/web/(\d+)(\w+_)?/(\S*)')
_WAYBACK_RELATIVE_SCHEME: Pattern = compile(r'(?<!://web.archive.org)/web/(\d+)(\w+_)?/(\S*)')
_TIMESTAMP_FORMAT: str = '%Y%m%d%H%M%S'


class ArchiveLink(BaseModel):
    timestamp: datetime
    original_url: AnyUrl
    category: str | None = None

    @property
    def url(self) -> str:
        """
        Obtain the original link found in the archive.org document.
        Returns: Original link.
        """
        category: str = f'{self.category}_' if self.category else ''
        return f'https://web.archive.org/web/{self.timestamp.strftime(_TIMESTAMP_FORMAT)}{category}/{self.original_url}'

    def __hash__(self) -> int:
        return hash(str(self.original_url))


class ArchivePage(BaseModel):
    archive_link: ArchiveLink
    content: bytes
    accessed: datetime = Field(default_factory=datetime.now)

    @property
    def category(self) -> str | None:
        return self.archive_link.category

    @property
    def encoded(self) -> dict[str, str | datetime | AnyUrl]:
        encoded_page = self.dict()
        encoded_page['content'] = b64encode(encoded_page['content']).decode('utf-8', 'replace')
        encoded_page['accessed'] = encoded_page['accessed'].isoformat()
        return encoded_page


def parse_link(
    url: str,
    scheme: Pattern = _WAYBACK_URL_SCHEME,
    relative_scheme: Pattern = _WAYBACK_RELATIVE_SCHEME,
    timestamp_format: str = _TIMESTAMP_FORMAT
) -> ArchiveLink:
    """
    Analyses an archive.org link such as https://web.archive.org/web/20220221051324/https://www.bundestag.de/ and
    extracts useful information such as timestamp and original url.

    Args:
        url: URL to be parsed
        scheme: Regular expression for absolute archive.org urls.
        relative_scheme: Regular expression for relative archive.org urls.
        timestamp_format: Timestamp format used in archive.org urls.
    Returns:
        ArchiveLink object providing timestamp, original_url and category for special links such as css or images.
    """
    analysis: Match | None = scheme.fullmatch(url) or relative_scheme.fullmatch(url)
    if not analysis:
        raise ValueError(f'{url} does not obey pattern {scheme.pattern} or {relative_scheme}')
    return ArchiveLink(
        timestamp=datetime.strptime(analysis.group(1), timestamp_format),
        category=category.strip('_') if (category := analysis.group(2)) else None,
        original_url=analysis.group(3)
    )


def find_links(
    content: str | list[str],
    scheme: Pattern = _WAYBACK_URL_SCHEME,
    relative_scheme: Pattern = _WAYBACK_RELATIVE_SCHEME
) -> Generator[ArchiveLink, None, None]:
    """
    Search for archive.org links in text or list of text. Use this function with caution in plain text documents, its
    primary usage is intended for HTML tag attributes.

    Args:
        content: Either a text or a list of text to be searched for links.
        scheme: Regular expression for absolute archive.org urls.
        relative_scheme: Regular expression for relative archive.org urls.
    Returns:
        Generator yielding all found archive.org links
    """
    content: list[str] = [content] if isinstance(content, str) else content
    for element in content:
        for match in chain(scheme.finditer(element), relative_scheme.finditer(element)):
            try:
                yield parse_link(match.group(), scheme)
            except ValidationError:
                continue


