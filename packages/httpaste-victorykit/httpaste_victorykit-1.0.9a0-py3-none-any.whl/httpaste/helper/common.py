from random import choice
from base64 import b64decode
from urllib.parse import urljoin
from importlib.resources import read_text
from tempfile import mkdtemp
from pathlib import Path
from contextlib import contextmanager


class DecodeError(Exception):
    """
    """


def generate_random_string(length: int, charset: str) -> str:

    return ''.join(choice(charset) for _ in range(length))


def decode(data: str, encoding: str) -> bytes:

    if encoding == 'base64':

        try:
            return b64decode(data.encode('ascii'))
        except UnicodeEncodeError as e:

            raise DecodeError('unable to decode with base64.') from e

    else:

        raise DecodeError(f'unknown encoding \'{encoding}\'.')


def join_url(base:str, url: str) -> str:

    return urljoin(base, url, True)


@contextmanager
def tmp_pkg_resource_text_path(package:str, resource:str) -> Path:
    """context manager for accessing package resources from a real path

        this applies to the circumstance of the package living inside of an
        egg and therefore is unable to provide real existing paths to any
        module that may require it.

        :param package: dot seperated package name
        :param resource: basename of resource inside package

        :returns: a Path-like object
    """
    data = read_text(package, resource)
    tmp_dirname = mkdtemp()
    tmp_dirpath = Path(tmp_dirname)
    tmp_file = tmp_dirpath.joinpath(resource)
    tmp_file.write_text(data)
    try:
        yield tmp_file
    finally:
        tmp_file.unlink()
        tmp_dirpath.rmdir()