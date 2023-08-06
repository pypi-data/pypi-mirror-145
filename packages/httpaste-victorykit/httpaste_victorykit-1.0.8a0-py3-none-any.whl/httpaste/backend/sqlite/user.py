"""SQlite backend user model interface
"""
from os import path
from sqlite3 import Connection
from httpaste.model import User
from importlib.resources import open_text


def load(proto: User, connection: Connection):
    """load a user
    """

    cur = connection.cursor()

    cur.execute(
        'SELECT sub, key_hash, paste_index FROM users WHERE sub=?', (proto.sub,))

    result = cur.fetchone()

    if result:

        return User(result['sub'], result['key_hash'], result['paste_index'])

    return None


def dump(model: User, connection: Connection):
    """dump a user
    """

    cur = connection.cursor()

    cur.execute('''INSERT OR REPLACE INTO users (sub, key_hash, paste_index)
                   VALUES (?,?,?)''', (model.sub, model.key_hash, model.index))

    connection.commit()


def delete(proto: object, connection: Connection) -> bool:

    cur = connection.cursor()

    cur.execute('''DELETE FROM users WHERE sub=?''', (proto.sub,))

    connection.commit()


def init(connection: Connection):

    cur = connection.cursor()

    with open_text('httpaste.backend.sqlite', 'user.sql') as fh:

        cur.execute(fh.read())

    connection.commit()


def sanitize(connection: Connection, model_class) -> bool:

    return None