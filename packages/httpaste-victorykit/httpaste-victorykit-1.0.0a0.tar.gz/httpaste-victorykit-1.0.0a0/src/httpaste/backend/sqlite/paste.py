"""SQlite backend paste model interface
"""
from os import path
from sqlite3 import Connection


def load(proto: object, connection: Connection, model_class: type):
    """load a paste
    """

    cur = connection.cursor()

    cur.execute(
        'SELECT pid, data, data_hash, sub, timestamp, lifetime, encoding FROM pastes WHERE pid=?',
        (proto.pid,
         ))

    result = cur.fetchone()

    if result:

        return model_class(
            result['pid'],
            result['sub'],
            result['data'],
            result['data_hash'],
            result['timestamp'],
            result['lifetime'],
            result['encoding'])

    return None


def dump(model: object, connection: Connection):
    """dump a paste
    """

    cur = connection.cursor()

    cur.execute(
        '''INSERT INTO pastes (pid, data, data_hash, sub, timestamp, lifetime, encoding)
                   VALUES (?,?,?,?,?,?,?)''',
        (model.pid,
         model.data,
         model.data_hash,
         model.sub,
         model.timestamp,
         model.lifetime,
         model.encoding))

    connection.commit()


def delete(proto: object, connection: Connection) -> bool:

    cur = connection.cursor()

    cur.execute('''DELETE FROM pastes WHERE pid=?''', (proto.pid,))

    connection.commit()


def init(connection: Connection):

    cur = connection.cursor()

    with open(path.join(path.dirname(__file__), 'paste.sql'), 'r') as fh:

        cur.execute(fh.read())

    connection.commit()
