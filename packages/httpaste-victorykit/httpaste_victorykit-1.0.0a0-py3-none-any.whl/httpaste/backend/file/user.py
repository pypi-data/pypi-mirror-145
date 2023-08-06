"""Filesystem backend user model interface

emulates a table database with base directory acting as the row, and files
acting as cells.
"""
from pathlib import Path
from ast import literal_eval


def load(
        proto: object,
        path: Path,
        model_class: type,
        model_schema: type) -> object:
    """load a paste
    """

    row = path.joinpath(proto.sub.hex())

    if not row.exists():

        return None

    cells = {}
    for column in ['key_hash', 'index']:

        cell = row.joinpath(column)

        if getattr(model_schema, column) == bytes:

            cells[column] = cell.read_bytes()
        else:

            cells[column] = literal_eval(cell.read_text())

    return model_class(
        proto.sub,
        cells['key_hash'],
        cells['index'])


def dump(model: object, path: Path, model_schema: object) -> None:
    """dump a paste
    """

    row = path.joinpath(model.sub.hex())
    row.mkdir(parents=True, exist_ok=True)

    for column in ['key_hash', 'index']:

        cell = row.joinpath(column)

        if getattr(model_schema, column) == bytes:

            cell.write_bytes(getattr(model, column))
        else:

            cell.write_text(getattr(model, column))


def delete(proto: object, path: Path) -> bool:
    """delete a paste
    """

    row = path.joinpath(proto.sub.hex())

    if row.exists():

        _rm_tree(row)


def init(path: Path):

    return None


def _rm_tree(pth: Path):
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()
