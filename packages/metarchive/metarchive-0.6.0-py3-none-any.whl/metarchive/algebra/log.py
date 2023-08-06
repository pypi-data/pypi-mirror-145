from typing import IO, Any, Iterable
from base64 import b64decode
from datetime import date, datetime
from json import dumps, loads
from metarchive.algebra.types import ArchivePage
from metarchive.algebra.analysis import DownloadError
from metarchive.algebra.acquisition import AcquisitionError


def adjust_value(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def adjust_result(result: dict[str, Any]) -> dict[str, Any]:
    return dict(
        (k, adjust_result(v) if isinstance(v, dict) else adjust_value(v))
        for (k, v) in result.items()
    )


def write_to_log(page: ArchivePage | DownloadError | AcquisitionError, log: IO[str]) -> None:
    log.write(dumps(adjust_result(page.encoded), ensure_ascii=False))
    log.write('\n')


def get_log_size(log: IO[str]) -> int:
    size: int = 0
    while True:
        line: str = log.readline()
        if not line:
            break
        else:
            size += 1
    return size


def read_from_log(log: IO[str]) -> ArchivePage | DownloadError | AcquisitionError | None:
    line: str = log.readline()
    if not line:
        return None
    content: dict[str, Any] = loads(line.strip())
    if 'error' in content:
        del content['error']
        if 'status_code' in content:
            return DownloadError(**content)
        else:
            error_type: type = __builtins__[content['original_error_type']]
            error_message: str = content['original_error_message']
            return AcquisitionError(error_type(error_message), content.get('archive_link', content.get('link')))
    else:
        content['content'] = b64decode(content['content'])
        return ArchivePage(**content)


def read_log(log: IO[str]) -> Iterable[ArchivePage | DownloadError | AcquisitionError]:
    while True:
        entry: ArchivePage | DownloadError | AcquisitionError | None = read_from_log(log)
        if entry is None:
            break
        else:
            yield entry
