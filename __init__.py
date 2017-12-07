"""PytSite File Plugin
"""
from pytsite import plugman as _plugman

# Public API
if _plugman.is_installed(__name__):
    from . import _model as model, _error as error, _driver as driver
    from ._api import create, get, get_multiple

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'
