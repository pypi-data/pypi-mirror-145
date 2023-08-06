from toolz import partial
from bs4 import BeautifulSoup
from metarchive.algebra.analysis import create_document_analyser, AnalyseDocument, create_url_analyser, AnalyseURL


def create_beautifulsoup_analyser(parser: str = 'html.parser') -> AnalyseDocument:
    """
    Creates a document analyser using the specified parser and Beautifulsoup4.

    Args:
        parser: Parser to use with BeautifulSoup
    Returns:
        The created analyser.
    """
    return create_document_analyser(partial(BeautifulSoup, features=parser), BeautifulSoup.find_all)


def create_beautifulsoup_url_analyser(parser: str = 'html.parser') -> AnalyseURL:
    """
    Creates an url analyser using the specified parser and Beautifulsoup4.

    Args:
        parser: Parser to use with BeautifulSoup
    Returns:
        The created analyser.
    """
    return create_url_analyser(partial(BeautifulSoup, features=parser), BeautifulSoup.find_all)
