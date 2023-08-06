from typing import Iterable
from argparse import ArgumentParser
from json import dump
from pathlib import Path
from tqdm import tqdm
from urllib.parse import urlparse
from metarchive.algebra.log import read_log, get_log_size
from metarchive.reconstruction.storage.directory import create_directory_store, StorePage, ArchivePage, PageID
from metarchive.reconstruction.links import transcribe_html_file, find_html_files


def translations(url: str) -> Iterable[str]:
    """
    Args:
        url:

    Returns:
    >>> for x in translations('https://web.archive.org/web/20220208000729/http://example.com/'):
    ...     print(x)
    """
    yield url
    yield urlparse(url).path



def main():
    parser: ArgumentParser = ArgumentParser('Reconstruct acquired page from log.')
    parser.add_argument('log_file')
    parser.add_argument('--target-dir', default=None)
    args = parser.parse_args()

    target_dir: Path = Path(args.target_dir) if args.target_dir else Path(f'{args.log_file}_reconstructed')
    target_dir.mkdir(parents=True, exist_ok=True)

    store_page: StorePage = create_directory_store(target_dir)
    translation: dict[str, str] = dict()
    start_page_id: PageID | None = None

    print("Acquiring log size")
    with open(args.log_file, encoding='utf-8') as src:
        size: int = get_log_size(src)
    progress: tqdm = tqdm(desc='Entries read from log', unit='entry', total=size)
    with open(args.log_file, encoding='utf-8') as src:
        for entry in read_log(src):
            if isinstance(entry, ArchivePage):
                page_id: PageID = store_page(entry)
                if not start_page_id:
                    start_page_id = page_id
                    with target_dir.joinpath('index.html').open('wb') as out:
                        out.write(entry.content)
                for potential_url in translations(entry.archive_link.url):
                    translation[potential_url] = f'/{page_id}'
            progress.update()
    with target_dir.joinpath('translation.json').open('w', encoding='utf-8') as out:
        dump(translation, out, indent=4)
    print("Start page: ", start_page_id)
    html_files: list[Path] = list(find_html_files(target_dir))
    progress: tqdm = tqdm(desc='HTML files transcribed', total=len(html_files), unit='files')
    for html_file in html_files:
        new_content: str = transcribe_html_file(html_file, translation)
        with html_file.open('w') as out:
            out.write(new_content)
        progress.update()


if __name__ == '__main__':
    main()