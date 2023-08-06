**Metarchive** was created during the need to analyse some archived sites from
http://archive.org to create some metrics. In this endeavor certain procedures repeated
itself over and over again, so I decided to put them to a package. In the spirit of Open Source
I decided to make the project public, maybe someone out there can cut some corners using it.
If so, great thing, let me know if you like to.

Please be reasonable when accessing pages archived by archive.org. It's a great project and there
is no need to create excessive stress on their servers. 

Below is a sample invocation of the library, for more information please have a look at the
documentation.

````python
from metarchive import create_url_analyser, AnalyseURL, ArchiveLink

analyse: AnalyseURL = create_url_analyser()
links: list[ArchiveLink] = list(
    analyse(
        'http://web.archive.org/web/20210101000012/http://example.com/'
    )
)
print(links)
# Will yield something like
[
    ArchiveLink(timestamp=datetime.datetime(2020, 11, 30, 23, 42, 54),
                original_url=AnyUrl('https://example.com/', scheme='https', host='example.com', tld='com',
                                    host_type='domain', path='/'), category=None),
    ArchiveLink(timestamp=datetime.datetime(2021, 2, 1, 0, 5, 5),
                original_url=AnyUrl('https://example.com/', scheme='https', host='example.com', tld='com',
                                    host_type='domain', path='/'), category=None),
    ArchiveLink(timestamp=datetime.datetime(2020, 12, 30, 23, 54, 41),
                original_url=AnyUrl('http://example.com/', scheme='http', host='example.com', tld='com',
                                    host_type='domain', path='/'), category=None),
    ArchiveLink(timestamp=datetime.datetime(2021, 1, 2, 0, 7, 38),
                original_url=AnyUrl('http://example.com/', scheme='http', host='example.com', tld='com',
                                    host_type='domain', path='/'), category=None),
    ArchiveLink(timestamp=datetime.datetime(2019, 12, 31, 23, 45, 1),
                original_url=AnyUrl('http://example.com/', scheme='http', host='example.com', tld='com',
                                    host_type='domain', path='/'), category=None),
    ArchiveLink(timestamp=datetime.datetime(2022, 1, 1, 0, 19, 39),
                original_url=AnyUrl('https://example.com/', scheme='https', host='example.com', tld='com',
                                    host_type='domain', path='/'), category=None),
    ArchiveLink(timestamp=datetime.datetime(2021, 1, 1, 0, 0, 12),
                original_url=AnyUrl('http://web.archive.org/screenshot/http://example.com/', scheme='http',
                                    host='web.archive.org', tld='org', host_type='domain',
                                    path='/screenshot/http://example.com/'), category=None),
    ArchiveLink(timestamp=datetime.datetime(2021, 1, 1, 0, 0, 12),
                original_url=AnyUrl('http://example.com/', scheme='http', host='example.com', tld='com',
                                    host_type='domain', path='/'), category=None),
    ArchiveLink(timestamp=datetime.datetime(2021, 1, 1, 0, 0, 12),
                original_url=AnyUrl('http://example.com/', scheme='http', host='example.com', tld='com',
                                    host_type='domain', path='/'), category=None),
    ArchiveLink(timestamp=datetime.datetime(2021, 1, 1, 0, 0, 12),
                original_url=AnyUrl('https://www.iana.org/domains/example', scheme='https', host='www.iana.org',
                                    tld='org', host_type='domain', path='/domains/example'), category=None)
]
````