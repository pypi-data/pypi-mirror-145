from uuid import uuid4
from metarchive.algebra.types import AnyUrl
from metarchive.algebra.storage import PageID, ArchivePage


def create_basic_id(page: ArchivePage) -> PageID:
    url: AnyUrl = page.archive_link.original_url
    file: str = url.path.strip('/').split('/')[-1]
    extension: str | None = file.rsplit('.', 1)[-1] if '.' in file else 'htm'
    return f'{uuid4()}.{extension}' if extension else f'{uuid4()}'

