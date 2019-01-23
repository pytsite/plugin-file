"""PytSite File Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _model as model, _error as error, _driver as driver
from ._api import create, get
from ._model import AbstractFile, AbstractImage


def plugin_load_wsgi():
    from pytsite import router

    from . import _controllers

    router.handle(_controllers.Download, '/file/download/<uid>', 'file@download')


def plugin_install():
    from plugins import assetman

    assetman.build(__name__)
