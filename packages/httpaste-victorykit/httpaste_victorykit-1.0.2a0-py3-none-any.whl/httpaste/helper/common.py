from random import choice
from base64 import b64decode
from urllib.parse import urljoin

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