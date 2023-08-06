#!/usr/bin/env python3
"""user model interface
"""
import json
from time import time
from typing import Optional

from httpaste import Config
from httpaste.helper.crypto import (
    dhash,
    shash,
    encrypt,
    decrypt,
    derive_key,
    DecryptionError)
from httpaste.model import (
    User,
    KeyHash,
    Index,
    SerializedIndex,
    Salt,
    PasteKey,
    PasteId,
    MasterKey,
    Sub)


class AuthenticationError(Exception):
    """Authentication Error
    """


class IndexError(Exception):
    """Index Decryption Error
    """


def _load(
        proto: User,
        master_key: str,
        backend: object,
        salt: Salt = Config.salt,
        hmac_iter: int = Config.hmac_iterations) -> Optional[User]:
    """load user model

        :param model: user model prototype
        :param master_key: user's master key
        :param backend: user model backend
        :param salt: randomization salt
    """

    model = backend.load(proto)

    if not model:
        return None

    try:
        serialized_data = decrypt(model.index, master_key, salt, hmac_iter)
    except DecryptionError as e:
        raise IndexError('unable to decrypt user index') from e
    else:
        data = json.loads(serialized_data)

    return User(
        *model[:-1],
        Index(**data)
    )


def _dump(
        model: User,
        key: MasterKey,
        backend: object,
        salt: Salt = Config.salt,
        hmac_iter: int = Config.hmac_iterations) -> None:
    """dump a user model

        :param model: user model
        :param key: user's master key
        :param backend: user model backend
        :param salt: randomization salt
    """

    if model.index is not None and not isinstance(model.index, dict):

        raise BaseException('index serialization pre-processing not allowed.')

    serialized_index = json.dumps(model.index).encode('utf-8')

    safe_index = SerializedIndex(encrypt(serialized_index, key, salt, hmac_iter))

    backend.dump(User(*model[:-1], safe_index))


def load_paste_key(
        pid: PasteId,
        sub: Sub,
        key: MasterKey,
        backend: object, salt: Salt = Config.salt, hmac_iter: int = Config.hmac_iterations) -> Optional[PasteKey]:
    """load a user paste key

        :param pid: paste id
        :param sub: user id
        :param key: user's master key
        :param backend: user model backend
        :param salt: randomization salt
    """

    model = _load(User(sub), key, backend, salt, hmac_iter)

    for k, v in model.index.get('pastes').items():

        if bytes.fromhex(k) == pid:

            return PasteKey(bytes.fromhex(v.get('key')))

    return None


def dump_paste_key(
        pid: PasteId,
        pkey: PasteKey,
        sub: Sub,
        key: MasterKey,
        backend: object,
        salt: str = Config.salt,
        hmac_iter: int = Config.hmac_iterations) -> None:
    """dump a user paste key

        :param pid: paste id
        :param key: paste key
        :param sub: user id
        :param key: user's master key
        :param backend: user model backend
    """

    model = _load(User(sub), key, backend, salt, hmac_iter)

    model.index.setdefault('pastes', {})[pid.hex()] = {
        'key': pkey.hex()
    }

    _dump(model, key, backend, salt, hmac_iter)


def authenticate(
        user_id: bytes,
        password: bytes,
        backend: object,
        salt: Salt = Config.salt,
        hmac_iter: int = Config.hmac_iterations):
    """authenticate a user

        :param user_id: human-readable user id
        :param password: clear text password
    """

    sub = Sub(dhash(user_id))
    key = MasterKey(derive_key(password, salt, hmac_iter))
    key_hash = KeyHash(dhash(key))

    proto = User(sub)

    bogus_decline_msg = 'unable to authenticate'

    try:
        model = _load(proto, key, backend, salt, hmac_iter)
    except IndexError as e:
        raise AuthenticationError(bogus_decline_msg) from e

    if not model:

        data = {
            'auth_expires': int(time()) + (1 * 60)
        }

        model = User(sub, key_hash, Index(data))
        _dump(model, key, backend, salt, hmac_iter)
    else:

        if model.key_hash != key_hash:

            raise AuthenticationError(bogus_decline_msg)

    return {
        'sub': sub,
        'master_key': key
    }


__all__ = [
    AuthenticationError,
    load_paste_key,
    dump_paste_key,
    authenticate
]