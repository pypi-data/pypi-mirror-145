"""Filesystem backend
"""
from os import path
from pathlib import Path
from typing import NamedTuple, Optional

from . import user
from . import paste


class Parameters(NamedTuple):
    """Filesystem backend parameters
    """

    #: path of base directory
    base_dirname: str
    #: basename of users table directory
    user_dirname: Optional[str] = 'users'
    #: basename of pastes table directory
    paste_dirname: Optional[str] = 'pastes'


class User(object):
    """Filesystem user model backend
    """

    dirname: Path
    path: Path

    def __init__(
            self,
            parameters: Parameters,
            model_class: type,
            model_schema: type):

        self.model_class = model_class

        self.model_schema = model_schema

        self.dirname = path.join(parameters.base_dirname,
                                 parameters.user_dirname)

        self.path = Path(self.dirname)

    def load(self, proto: object):

        return user.load(proto, self.path, self.model_class, self.model_schema)

    def dump(self, model: object):

        return user.dump(model, self.path, self.model_schema)

    def delete(self, proto: object):

        return user.delete(proto, self.path)

    def init(self):

        return user.init(self.path)

    def sanitize(self):

        if self.path.exists():
            return user.sanitize(self.path, self.model_class, self.model_schema)

        return None


class Paste(object):
    """Filesystem paste model backend
    """

    dirname: str
    path: Path

    def __init__(
            self,
            parameters: Parameters,
            model_class: type,
            model_schema: type):

        self.model_class = model_class

        self.model_schema = model_schema

        self.dirname = path.join(parameters.base_dirname,
                                 parameters.paste_dirname)

        self.path = Path(self.dirname)

    def load(self, proto: object):

        return paste.load(proto, self.path, self.model_class, self.model_schema)

    def dump(self, model: object):

        return paste.dump(model, self.path, self.model_schema)

    def delete(self, proto: object):

        return paste.delete(proto, self.path)

    def init(self):

        return paste.init(self.path)

    def sanitize(self):

        if self.path.exists():
            return paste.sanitize(self.path, self.model_class, self.model_schema)

        return None