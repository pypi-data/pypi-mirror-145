# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metarchive',
 'metarchive.algebra',
 'metarchive.analysis',
 'metarchive.analysis.engines',
 'metarchive.aquicision',
 'metarchive.interface',
 'metarchive.interface.console',
 'metarchive.interface.helper',
 'metarchive.reconstruction',
 'metarchive.reconstruction.storage']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'more-itertools>=8.12.0,<9.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-magic>=0.4.25,<0.5.0',
 'requests>=2.27.1,<3.0.0',
 'toolz>=0.11.2,<0.12.0',
 'tqdm>=4.63.0,<5.0.0']

setup_kwargs = {
    'name': 'metarchive',
    'version': '0.6.1',
    'description': 'Tool for analysing links within a website archived by archive.org',
    'long_description': "**Metarchive** was created during the need to analyse some archived sites from\nhttp://archive.org to create some metrics. In this endeavor certain procedures repeated\nitself over and over again, so I decided to put them to a package. In the spirit of Open Source\nI decided to make the project public, maybe someone out there can cut some corners using it.\nIf so, great thing, let me know if you like to.\n\nPlease be reasonable when accessing pages archived by archive.org. It's a great project and there\nis no need to create excessive stress on their servers. \n\nBelow is a sample invocation of the library, for more information please have a look at the\ndocumentation.\n\n````python\nfrom metarchive import create_url_analyser, AnalyseURL, ArchiveLink\n\nanalyse: AnalyseURL = create_url_analyser()\nlinks: list[ArchiveLink] = list(\n    analyse(\n        'http://web.archive.org/web/20210101000012/http://example.com/'\n    )\n)\nprint(links)\n# Will yield something like\n[\n    ArchiveLink(timestamp=datetime.datetime(2020, 11, 30, 23, 42, 54),\n                original_url=AnyUrl('https://example.com/', scheme='https', host='example.com', tld='com',\n                                    host_type='domain', path='/'), category=None),\n    ArchiveLink(timestamp=datetime.datetime(2021, 2, 1, 0, 5, 5),\n                original_url=AnyUrl('https://example.com/', scheme='https', host='example.com', tld='com',\n                                    host_type='domain', path='/'), category=None),\n    ArchiveLink(timestamp=datetime.datetime(2020, 12, 30, 23, 54, 41),\n                original_url=AnyUrl('http://example.com/', scheme='http', host='example.com', tld='com',\n                                    host_type='domain', path='/'), category=None),\n    ArchiveLink(timestamp=datetime.datetime(2021, 1, 2, 0, 7, 38),\n                original_url=AnyUrl('http://example.com/', scheme='http', host='example.com', tld='com',\n                                    host_type='domain', path='/'), category=None),\n    ArchiveLink(timestamp=datetime.datetime(2019, 12, 31, 23, 45, 1),\n                original_url=AnyUrl('http://example.com/', scheme='http', host='example.com', tld='com',\n                                    host_type='domain', path='/'), category=None),\n    ArchiveLink(timestamp=datetime.datetime(2022, 1, 1, 0, 19, 39),\n                original_url=AnyUrl('https://example.com/', scheme='https', host='example.com', tld='com',\n                                    host_type='domain', path='/'), category=None),\n    ArchiveLink(timestamp=datetime.datetime(2021, 1, 1, 0, 0, 12),\n                original_url=AnyUrl('http://web.archive.org/screenshot/http://example.com/', scheme='http',\n                                    host='web.archive.org', tld='org', host_type='domain',\n                                    path='/screenshot/http://example.com/'), category=None),\n    ArchiveLink(timestamp=datetime.datetime(2021, 1, 1, 0, 0, 12),\n                original_url=AnyUrl('http://example.com/', scheme='http', host='example.com', tld='com',\n                                    host_type='domain', path='/'), category=None),\n    ArchiveLink(timestamp=datetime.datetime(2021, 1, 1, 0, 0, 12),\n                original_url=AnyUrl('http://example.com/', scheme='http', host='example.com', tld='com',\n                                    host_type='domain', path='/'), category=None),\n    ArchiveLink(timestamp=datetime.datetime(2021, 1, 1, 0, 0, 12),\n                original_url=AnyUrl('https://www.iana.org/domains/example', scheme='https', host='www.iana.org',\n                                    tld='org', host_type='domain', path='/domains/example'), category=None)\n]\n````",
    'author': 'Patrick Greß',
    'author_email': 'patrick.daniel.gress@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/patrick.daniel.gress/osmium',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
