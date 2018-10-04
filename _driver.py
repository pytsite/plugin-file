"""Abstract File Driver
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC as _ABC, abstractmethod as _abstractmethod
from . import _model


class Abstract(_ABC):
    @_abstractmethod
    def create(self, file_path: str, mime: str, name: str = None, description: str = None, propose_path: str = None,
               **kwargs) -> _model.AbstractFile:
        pass

    @_abstractmethod
    def get(self, uid: str) -> _model.AbstractFile:
        pass
