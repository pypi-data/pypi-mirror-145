"""SQLite backend
"""
from sqlite3 import Connection, Row, connect
from typing import NamedTuple, Optional

from . import user
from . import paste


class Parameters(NamedTuple):
    """SQLite backend parameters
    """

    #: local path or URI
    path: str
    #: a sqlite3.Connection object (does not apply to config)
    connection: Optional[object] = None


class User(object):
    """SQLite user model backend
    """

    connection: Connection

    def __init__(self, parameters: Parameters, model_class: type):

        self.model_class = model_class

        self.connection = get_connection(parameters)

    def load(self, proto: object):

        return user.load(proto, self.connection, self.model_class)

    def dump(self, model: object):

        return user.dump(model, self.connection)

    def delete(self, proto: object):

        return user.delete(proto, self.connection)

    def init(self):

        return user.init(self.connection)

    def sanitize(self):

        return user.sanitize(self.connection, self.model_class)


class Paste(object):
    """SQLite paste model backend
    """

    connection: Connection

    def __init__(self, parameters: Parameters, model_class: type):

        self.model_class = model_class

        self.connection = get_connection(parameters)

    def load(self, proto: object):

        return paste.load(proto, self.connection, self.model_class)

    def dump(self, model: object):

        return paste.dump(model, self.connection)

    def delete(self, proto: object):

        return paste.delete(proto, self.connection)

    def init(self):

        return paste.init(self.connection)

    def sanitize(self):

        return paste.sanitize(self.connection, self.model_class)


def get_connection(parameters: Parameters):
    """get an sqlite connection object
    """

    if parameters.connection:

        return parameters.connection

    connection = connect(parameters.path, check_same_thread=False)
    connection.row_factory = Row

    return connection
