from typing import Callable
from pathlib import Path
from metarchive.algebra.storage import StorePage, ArchivePage, PageID
from metarchive.reconstruction.storage.basic import create_basic_id


def create_directory_store(
    directory: Path,
    create_id: Callable[[ArchivePage], PageID] = create_basic_id
) -> StorePage:

    def store_page(page: ArchivePage) -> PageID:
        page_id: PageID = create_id(page)
        with directory.joinpath(page_id).open('wb') as out:
            out.write(page.content)
        return page_id

    return store_page
