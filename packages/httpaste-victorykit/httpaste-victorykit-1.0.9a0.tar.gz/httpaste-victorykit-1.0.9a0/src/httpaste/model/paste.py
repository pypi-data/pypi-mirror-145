#!/usr/bin/env python3
"""paste model interface
"""
import json
from typing import Optional, Tuple
import time

from httpaste import Config
from httpaste.helper.crypto import dhash, shash, encrypt, decrypt
from httpaste.helper.common import generate_random_string
from httpaste.model import (Paste, PasteId, Sub, MasterKey, PasteKey, Salt,
                            PasteData, PasteHash, PasteTimestamp, PasteSub,
                            PasteLifetime, PasteEncoding, PasteExpiration)


class NotFoundError(Exception):
    """Paste Exception
    """


class SubError(Exception):
    """Paste Sub Exception
    """


class ChecksumError(Exception):
    """Paste Checksum Exception
    """


class LifetimeError(Exception):
    """Paste Lifetime Exception
    """


class BackendError(Exception):
    """
    """


def generate_paste_id(
        length: int = Config.paste_id_size,
        charset: str = Config.paste_id_charset) -> bytes:
    """generate a paste id

        :param length: length of id
        :param charset: character set of id
    """

    return generate_random_string(length, charset).encode('utf-8')


def generate_paste_key(
        length: int = Config.paste_key_size,
        charset: str = Config.paste_key_charset) -> bytes:
    """generate a paste encryption key

        :param length: length of key
        :param charset: character set of key
    """

    return generate_random_string(length, charset).encode('utf-8')


def load(proto: Paste, backend: object) -> Optional[Paste]:
    """load a paste model

        :param proto: paste model prototype
        :param backend: model backend object
    """

    safe_pid = PasteId(dhash(proto.pid))

    try:
        model = backend.load(Paste(safe_pid))
    except Exception as e:
        raise BackendError(f'{e.__class__.__name__}: {e}') from e

    if not model:

        raise NotFoundError('Paste does not exist')

    if proto.sub and model.sub != shash(
            proto.sub,
            model.data_hash,
            proto.pid) or not proto.sub and model.sub:

        raise SubError('Paste not owned by user')

    if model.expiration > 0 and model.expiration < int(time.time()):

        raise LifetimeError('Paste expired')

    return model


def load_safe(
        proto: Paste,
        key: PasteKey,
        backend: object,
        salt: Salt = Config.salt,
        hmac_iter: int = Config.hmac_iterations):
    """load an encrypted paste model

        :param proto: paste model prototype
        :param paste_key: paste encryption key
        :param backend: model backend object
    """

    model = load(proto, backend)

    data = decrypt(model.data, key, salt, hmac_iter)

    if model.data_hash and dhash(data) != model.data_hash:

        raise ChecksumError('Paste data scrambled')

    return Paste(
        proto.pid,
        proto.sub,
        data,
        model.data_hash,
        model.expiration,
        model.encoding)


def dump(model: Paste, backend: object) -> None:
    """dump a paste model

        :param model: paste model
        :param backend: model backend object
    """

    try:
        backend.dump(model)
    except Exception as e:
        raise BackendError(str(e)) from e


def delete(proto: Paste, backend: object) -> None:
    """delete a paste model
    """

    try:
        model = load(proto, backend)
    except LifetimeError:
        pass

    safe_pid = PasteId(dhash(proto.pid))

    try:
        backend.delete(Paste(safe_pid))
    except Exception as e:
        raise BackendError(str(e)) from e


def delete_safe(
        proto: Paste,
        key: PasteKey,
        backend: object,
        salt: Salt = Config.salt,
        hmac_iter: int = Config.hmac_iterations) -> None:
    """
    """

    try:
        model = load_safe(proto, key, backend, salt, hmac_iter)
    except LifetimeError:
        pass

    safe_pid = PasteId(dhash(proto.pid))

    backend.delete(Paste(safe_pid))


def create(
        data: PasteData,
        lifetime: PasteLifetime,
        encoding: PasteEncoding,
        backend: object,
        salt: Salt = Config.salt,
        hmac_iter: int = Config.hmac_iterations) -> PasteId:
    """create an unencrypted paste

        :param data: paste data
        :param lifetime: paste expiration (in minutes)
        :param backend: model backend object
    """

    pid = PasteId(generate_paste_id())
    safe_pid = PasteId(dhash(pid))
    data_hash = PasteHash(dhash(data))
    sub = None
    timestamp = PasteTimestamp(int(time.time()))

    if lifetime < 0:
        expiration = -1
    else:
        expiration = PasteExpiration(timestamp + (lifetime * 60))

    safe_data = PasteData(encrypt(data, pid, salt, hmac_iter))

    model = Paste(
        safe_pid,
        sub,
        safe_data,
        data_hash,
        expiration,
        encoding)

    dump(model, backend)

    return pid


def create_safe(data: PasteData,
                lifetime: PasteLifetime,
                sub: Sub,
                encoding: PasteEncoding,
                backend: object,
                salt: Salt = Config.salt,
                hmac_iter: int = Config.hmac_iterations) -> Tuple[PasteId,PasteKey]:
    """create an encrypted paste

        :param data: paste data
        :param lifetime: paste expiration (in minutes)
        :param sub: paste owner id
        :param backend: model backend object
        :param salt: randomization salt
    """

    pid = PasteId(generate_paste_id())
    safe_pid = PasteId(dhash(pid))
    pkey = PasteKey(generate_paste_key())
    data_hash = PasteHash(dhash(data))
    safe_sub = PasteSub(shash(sub, data_hash, pid))
    timestamp = PasteTimestamp(int(time.time()))

    if lifetime < 0:
        expiration = -1
    else:
        expiration = PasteExpiration(timestamp + (lifetime * 60))

    safe_data = PasteData(encrypt(data, pkey, salt, hmac_iter))

    dump(Paste(
        safe_pid,
        safe_sub,
        safe_data,
        data_hash,
        expiration,
        encoding
    ), backend)

    return pid, pkey


def remove(pid: PasteId, backend: object):
    """conveniently delete an unencrypted paste
    """

    proto = Paste(pid)

    delete(proto, backend)


def remove_safe(
        pid: PasteId,
        sub: Sub,
        key: PasteKey,
        backend: object,
        salt: Salt = Config.salt,
        hmac_iter: int = Config.hmac_iterations):

    proto = Paste(pid, sub)

    delete_safe(proto, key, backend, salt, hmac_iter)


def get(pid: PasteId, backend: object, salt: Salt = Config.salt, hmac_iter: int = Config.hmac_iterations) -> PasteData:
    """conveniently load an unencrypted paste
    """

    model = load(Paste(pid), backend)

    data = decrypt(model.data, pid, salt, hmac_iter)

    return PasteData(data), model.expiration, model.encoding


def get_safe(
        pid: PasteId,
        pkey: PasteKey,
        sub: Sub,
        backend: object,
        salt: Salt = Config.salt,
        hmac_iter: int = Config.hmac_iterations) -> PasteData:
    """conveniently load an encrypted paste
    """

    model = load_safe(Paste(pid, sub), pkey, backend, salt, hmac_iter)

    return PasteData(model.data), model.expiration, model.encoding
