from typing import Iterable, Callable, IO
from pathlib import Path
from urllib.parse import urlparse
from os import scandir, DirEntry
from toolz import identity
from magic import Magic
from bs4 import BeautifulSoup

HTML_MIMES: set[str] = {'text/html'}


def find_html_files(directory: Path) -> Iterable[Path]:
    get_mime: Magic = Magic(mime=True)
    for file in filter(DirEntry.is_file, scandir(directory)):
        mime_type = get_mime.from_file(file.path)
        if mime_type in HTML_MIMES:
            yield directory.joinpath(file.name)


def silence_other_archive_links(link: str | tuple[str]) -> str | tuple[str]:
    if isinstance(link, tuple):
        return tuple(map(silence_other_archive_links, link))
    parsed_url = urlparse(link)
    if parsed_url.hostname and parsed_url.hostname.endswith('archive.org'):
        return '/silenced'
    else:
        return link


def transcribe_html_file(
    html_file: Path | IO[str],
    translation: dict[str, str],
    default: Callable[[str], str] = silence_other_archive_links
) -> str:
    with (html_file.open('rb') if isinstance(html_file, Path) else html_file) as src:
        soup: BeautifulSoup = BeautifulSoup(src.read())
        for element in soup.find_all(True):
            for attribute, value in element.attrs.items():
                if isinstance(value, list):
                    value = tuple(value)
                element.attrs[attribute] = translation.get(value, default(value))
    return soup.prettify()
