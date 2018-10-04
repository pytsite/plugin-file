"""PytSite File Plugin Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class FileNotFound(FileNotFoundError, Error):
    pass


class InvalidFileUidFormat(Error):
    pass
