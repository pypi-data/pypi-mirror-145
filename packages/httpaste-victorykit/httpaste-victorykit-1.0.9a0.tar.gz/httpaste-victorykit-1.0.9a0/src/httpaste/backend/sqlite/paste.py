"""SQlite backend paste model interface
"""
from os import path
from sqlite3 import Connection
from time import time
from importlib.resources import open_text


def load(proto: object, connection: Connection, model_class: type):
    """load a paste
    """

    cur = connection.cursor()

    cur.execute(
        'SELECT pid, data, data_hash, sub, expiration, encoding FROM pastes WHERE pid=?',
        (proto.pid,
         ))

    result = cur.fetchone()

    if result:

        return model_class(
            result['pid'],
            result['sub'],
            result['data'],
            result['data_hash'],
            result['expiration'],
            result['encoding'])

    return None


def dump(model: object, connection: Connection):
    """dump a paste
    """

    cur = connection.cursor()

    cur.execute(
        '''INSERT INTO pastes (pid, data, data_hash, sub, expiration, encoding)
                   VALUES (?,?,?,?,?,?)''',
        (model.pid,
         model.data,
         model.data_hash,
         model.sub,
         model.expiration,
         model.encoding))

    connection.commit()


def delete(proto: object, connection: Connection) -> bool:

    cur = connection.cursor()

    cur.execute('''DELETE FROM pastes WHERE pid=?''', (proto.pid,))

    connection.commit()


def init(connection: Connection):

    cur = connection.cursor()

    with open_text('httpaste.backend.sqlite', 'paste.sql') as fh:

        cur.execute(fh.read())

    connection.commit()


def sanitize(connection: Connection, model_class: type) -> bool:

    cur = connection.cursor()

    cur.execute('''SELECT pid FROM pastes WHERE expiration < ? AND expiration > 0''', (int(time()),))

    for row in cur.fetchall():

        delete(model_class(row['pid']))