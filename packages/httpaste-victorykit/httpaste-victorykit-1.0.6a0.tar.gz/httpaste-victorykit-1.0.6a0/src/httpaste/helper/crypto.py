#!/usr/bin/env python3
"""Cryptography
"""
import hashlib
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

from httpaste import Config


DEFAULT_HMAC_ITERATIONS = 20000


class DecryptionError(Exception):
    """
    """


def shash(data: bytes, key: bytes, salt: bytes):
    """get a signed/keyed/salted data hash

        :param data: bytes to hash
        :oaram
    """

    return hashlib.blake2b(data, key=key, salt=salt).digest()


def dhash(data: bytes):
    """get a data hash

        :param data: bytes to hash
    """

    return hashlib.sha512(data).digest()


def derive_key(main_key: str, salt: bytes = Config.salt, iterations:int=DEFAULT_HMAC_ITERATIONS) -> bytes:
    """derive a key from a main key

        :param main_key: main key to derive from
        :param salt: randomization salt
    """

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )

    return base64.urlsafe_b64encode(kdf.derive(main_key))


def encrypt(data: bytes, key: bytes, salt: bytes, hmac_iterations:int=DEFAULT_HMAC_ITERATIONS) -> bytes:
    """encrypt a data block

        :param data: data block
        :param key: password to encrypt with
        :param salt: randomization salt
    """

    return Fernet(derive_key(key, salt, hmac_iterations)).encrypt(data)


def decrypt(data: bytes, key: bytes, salt: bytes, hmac_iterations:int=DEFAULT_HMAC_ITERATIONS):
    """encrypt a data block

        :param data: data block
        :param key: password to encrypt with
        :param salt: randomization salt
    """

    try:

        return Fernet(derive_key(key, salt, hmac_iterations)).decrypt(data)

    except InvalidToken as e:

        raise DecryptionError('unable to decrypt') from e
