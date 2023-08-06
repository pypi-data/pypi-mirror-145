from typing import Protocol, TypeAlias
from metarchive.algebra.types import ArchivePage


PageID: TypeAlias = str


class StorePage(Protocol):
    def __call__(self, page: ArchivePage) -> PageID: ...


class LoadPage(Protocol):
    def __call__(self, page_id: PageID) -> ArchivePage: ...


