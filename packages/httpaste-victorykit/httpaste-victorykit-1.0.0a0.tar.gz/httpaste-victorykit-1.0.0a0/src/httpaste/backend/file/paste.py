"""Filesystem backend paste model interface

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

    row = path.joinpath(proto.pid.hex())

    if not row.exists():

        return None

    cells = {}
    for column in [
        'data',
        'data_hash',
        'sub',
        'timestamp',
        'lifetime',
        'encoding']:

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
        cells['timestamp'],
        cells['lifetime'],
        cells['encoding'])


def dump(model: object, path: Path, model_schema: type) -> None:
    """dump a paste
    """

    row = path.joinpath(model.pid.hex())
    row.mkdir(parents=True, exist_ok=True)

    for column in [
        'data',
        'data_hash',
        'sub',
        'timestamp',
        'lifetime',
            'encoding']:

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


def _rm_tree(pth: Path):
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()
