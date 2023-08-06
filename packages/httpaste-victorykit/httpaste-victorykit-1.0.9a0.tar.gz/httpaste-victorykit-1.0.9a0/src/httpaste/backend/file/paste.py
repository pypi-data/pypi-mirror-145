"""Filesystem backend paste model interface

emulates a table database with base directory acting as the row, and files
acting as cells.
"""
from pathlib import Path
from ast import literal_eval
from time import time


COLUMNS = [
    'data',
    'data_hash',
    'sub',
    'expiration',
    'encoding'
]


def load(
        proto: object,
        path: Path,
        model_class: type,
        model_schema: type) -> object:
    """load a paste
    """

    row = path.joinpath(proto.pid.hex())

    if not row.exists():

        return None

    cells = {}
    for column in COLUMNS:

        cell = row.joinpath(column)

        try:
            cell_schema = getattr(model_schema, column)
        except AttributeError:
            raise RuntimeError(
                'Schema {model_schema.__name__} has no attribute {column}'
            )

        if not cell.exists():
            cells[column] = None
        elif cell_schema == bytes:
            cells[column] = cell.read_bytes()
        elif cell_schema == str:
            cells[column] = cell.read_text()
        else:
            try:
                cells[column] = literal_eval(cell.read_text())
            except ValueError as e:
                raise ValueError(f'error evaluating column [{column}]') from e

    return model_class(
        proto.pid,
        cells['sub'],
        cells['data'],
        cells['data_hash'],
        cells['expiration'],
        cells['encoding'])


def dump(model: object, path: Path, model_schema: type) -> None:
    """dump a paste
    """

    row = path.joinpath(model.pid.hex())
    row.mkdir(parents=True, exist_ok=True)

    for column in COLUMNS:

        cell = row.joinpath(column)
        cell_schema = getattr(model_schema, column)
        cell_value = getattr(model, column)

        if not cell_value:
            continue
        elif cell_schema == bytes:
            cell.write_bytes(getattr(model, column))
        else:
            cell.write_text(str(getattr(model, column)))


def delete(proto: object, path: Path) -> bool:

    row = path.joinpath(proto.pid.hex())

    if row.exists():

        _rm_tree(row)


def init(path: Path):

    return None


def sanitize(path: Path, model_class: type, model_schema: type):

    for row in path.iterdir():

        expiration_cell = row.joinpath('expiration')

        if not expiration_cell.exists():
            continue

        expiration = literal_eval(expiration_cell.read_text())

        if expiration < int(time()) and expiration > 0:

            delete(model_class(bytes.fromhex(row.name)), path)


def _rm_tree(pth: Path):
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()
