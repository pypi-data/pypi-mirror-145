"""Backend Interfaces

implements backend of model
"""
import sys
from inspect import isclass
from typing import Dict, Tuple

from httpaste.model import Backend, UserDataSchema, PasteDataSchema, User, Paste
from .sqlite import Parameters as SqliteParameters
from .sqlite import User as SqliteUser
from .sqlite import Paste as SqlitePaste
from .sqlite import get_connection as get_sqlite_connection
from .file import Parameters as FileParameters
from .file import User as FileUser
from .file import Paste as FilePaste


class SQLite(Backend):
    """SQLite backend interface
    """

    parameter_class = SqliteParameters
    user: SqliteUser
    paste: SqlitePaste

    def __init__(self, parameters: SqliteParameters):

        parameters = SqliteParameters(parameters.path, get_sqlite_connection(parameters))

        self.user = SqliteUser(parameters, User)
        self.paste = SqlitePaste(parameters, Paste)


class File(Backend):
    """File backend interface
    """

    parameter_class = FileParameters
    user: FileUser
    paste: FilePaste

    def __init__(self, parameters: FileParameters):

        self.user = FileUser(parameters, User, UserDataSchema)
        self.paste = FilePaste(parameters, Paste, PasteDataSchema)


def get_backend_map() -> Dict[str, Tuple[type, type]]:
    """get a map of backend ids and their classes
    """

    mod = sys.modules[__name__]
    out = {}

    for i in dir(mod):

        obj = getattr(mod, i)

        if isclass(obj) and obj.__module__ == __name__:

            out[i.lower()] = (obj, obj.parameter_class)

    return out
