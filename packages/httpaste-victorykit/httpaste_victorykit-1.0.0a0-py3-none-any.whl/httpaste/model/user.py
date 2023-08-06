#!/usr/bin/env python3
"""user model interface
"""
import json
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


def load(
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
        return User(
            *model[:-1],
            Index(**json.loads(decrypt(model.index, master_key, salt, hmac_iter)))
        )
    except DecryptionError as e:

        raise IndexError('unable to decrypt user index') from e


def dump(
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

    if not isinstance(model.index, Index):

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

    for k, v in load(User(sub), key, backend, salt, hmac_iter).index.items():

        if bytes.fromhex(k) == pid:

            return PasteKey(bytes.fromhex(v))

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

    model = load(User(sub), key, backend, salt, hmac_iter)

    dump(User(*model[:-1], Index({
        **model.index,
        **{pid.hex(): pkey.hex()}
    })), key, backend, salt, hmac_iter)


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

    try:
        model = load(proto, key, backend, salt, hmac_iter)
    except IndexError as e:
        raise AuthenticationError('you dun goofed')

    if not model:

        model = User(sub, key_hash, Index({}))
        dump(model, key, backend, salt, hmac_iter)
    else:

        if model.key_hash != key_hash:

            raise AuthenticationError('you dun goofed')

    return {
        'sub': sub,
        'master_key': key
    }
