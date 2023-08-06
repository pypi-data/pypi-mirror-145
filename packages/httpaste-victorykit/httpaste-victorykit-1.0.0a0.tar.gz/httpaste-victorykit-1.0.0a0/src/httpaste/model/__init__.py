"""Model
"""
from typing import NamedTuple, Optional, Dict, Union


class PasteDataSchema:
    """Paste Interface schema between Model and Backend
    """
    pid = bytes
    data = bytes
    data_hash = bytes
    sub = bytes
    timestamp = int
    lifetime = int
    encoding = str


class UserDataSchema:
    """User Interface Schema between Model and Backend
    """
    sub = bytes
    key_hash = bytes
    index = bytes


class Backend(object):
    """Backend
    """
    parameter_class: str


class Salt(bytes):
    """Salt
    """


class PasteData(PasteDataSchema.data):
    """Paste Data
    """


class PasteHash(PasteDataSchema.data_hash):
    """Paste Data Hash
    """


class PasteTimestamp(PasteDataSchema.timestamp):
    """Paste Timestamp
    """


class PasteEncoding(PasteDataSchema.encoding):
    """
    """


class PasteLifetime(PasteDataSchema.lifetime):
    """Paste Lifetime
    """


class PasteSub(PasteDataSchema.sub):
    """Hashed user id
    """


class KeyHash(UserDataSchema.key_hash):
    """User Master Key Hash
    """


class PasteKey(bytes):
    """Paste encryption key
    """


class PasteId(PasteDataSchema.pid):
    """Paste unique identifier
    """


class MasterKey(bytes):
    """User's master encryption key
    """


class Sub(UserDataSchema.sub):
    """User id
    """


class Index(Dict[PasteId, PasteKey]):
    """User Paste Index
    """


class SerializedIndex(UserDataSchema.index):
    """User Paste Index (serialized)
    """


class User(NamedTuple):
    """Global User Model (and Prototype)

        non-optional values are prototype values
    """

    #: user id
    sub: Sub
    #: user's master key hash
    key_hash: Optional[KeyHash] = None
    #: user's paste index
    index: Optional[Union[Index, SerializedIndex]] = None


class Paste(NamedTuple):
    """Global Paste Model (and Prototype)

        non-optional values are prototype values
    """

    #: paste id
    pid: PasteId
    #: paste owner
    sub: Optional[PasteSub] = None
    #: paste data
    data: Optional[PasteData] = None
    #: paste data hash
    data_hash: Optional[PasteHash] = None
    #: paste timestamp
    timestamp: Optional[PasteTimestamp] = None
    #: paste lifetime
    lifetime: Optional[PasteLifetime] = None
    #: paste encoding
    encoding: Optional[PasteEncoding] = None
