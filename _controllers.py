"""PytSite File Plugin Controllers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import routing as _routing
from . import _api


class Download(_routing.Controller):
    def exec(self):
        f = _api.get(self.arg('uid'))

        return self.file(f.storage_path, f.name, f.mime)
