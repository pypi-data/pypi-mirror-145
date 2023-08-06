from typing import Iterable
from metarchive.algebra.types import ArchiveLink, ArchivePage
from metarchive.algebra.analysis import DownloadError, download, AnalyseDocument, TagPredicate, AllTags
from metarchive.algebra.acquisition import AcquisitionError, AcquireLink
from metarchive.analysis.engines.beautifulsoup import create_beautifulsoup_analyser


def create_basic_acquisition(
    analyze: AnalyseDocument = create_beautifulsoup_analyser(),
    predicate: TagPredicate = AllTags
) -> AcquireLink:
    def basic_acquisition(link: ArchiveLink) -> Iterable[ArchiveLink | ArchivePage | DownloadError | AcquisitionError]:
        try:
            page: ArchivePage = ArchivePage(content=download(link), archive_link=link)
            yield page
            if not link.category:
                for follow_up in analyze(page.content, predicate):
                    yield follow_up
        except DownloadError as error:
            yield error
        except Exception as error:
            yield AcquisitionError(error, link)
    return basic_acquisition


