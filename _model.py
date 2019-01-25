"""PytSite File Plugin Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Any as _Any
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from os import path as _path
from pytsite import util as _util, router as _router
from plugins import assetman as _assetman

_THUMBS = ('ai', 'avi', 'css', 'csv', 'dbf', 'doc', 'dwg', 'exe', 'file', 'fla', 'html', 'iso', 'jpg', 'json', 'js',
           'mp3', 'mp4', 'pdf', 'png', 'ppt', 'psd', 'rtf', 'svg', 'txt', 'xls', 'xml', 'zip')

_EXT_THUMB = {
    'htm': 'html',
    'jpe': 'jpg',
    'jpeg': 'jpg',
    'jif': 'jpg',
    'jfif': 'jpg',
    'jfi': 'jpg',
    'jp2': 'jpg',
    'j2k': 'jpg',
    'jpf': 'jpg',
    'jpx': 'jpg',
    'jpm': 'jpg',
    'mj2': 'jpg',
    'docx': 'doc',
    'odt': 'doc',
    'xlsx': 'xls',
    'ods': 'xls',
}


class AbstractFile(_ABC):
    @property
    def uid(self) -> str:
        """Get UID of the file
        """
        return self.get_field('uid')

    @uid.setter
    def uid(self, value: str):
        """Set UID of the file
        """
        raise RuntimeError("'uid' property is read-only")

    @property
    def length(self) -> int:
        """Get length of the file in bytes
        """
        return self.get_field('length')

    @length.setter
    def length(self, value: int):
        """Set length of the file in bytes
        """
        self.set_field('length', value)

    @property
    def path(self) -> str:
        """Get path of the file relative to storage
        """
        return self.get_field('path')

    @path.setter
    def path(self, value: str):
        """Set path of the file relative to storage
        """
        self.set_field('path', value)

    @property
    def storage_path(self) -> str:
        """Get path of the file in the storage
        """
        return self.get_field('storage_path')

    @storage_path.setter
    def storage_path(self, value: str):
        """Set path of the file in the storage
        """
        self.set_field('storage_path', value)

    @property
    def ext(self) -> str:
        """Get extension of the file
        """
        if not self.path:
            raise ValueError('File path is empty')

        return _path.splitext(self.path)[1]

    @property
    def name(self) -> str:
        """Get name of the file
        """
        return self.get_field('name')

    @name.setter
    def name(self, value: str):
        """Set name of the file
        """
        self.set_field('name', value)

    @property
    def description(self) -> str:
        """Get description of the file
        """
        return self.get_field('description')

    @description.setter
    def description(self, value: str):
        """Set description of the file
        """
        self.set_field('description', value)

    @property
    def mime(self) -> str:
        """Get MIME of the file
        """
        return self.get_field('mime')

    @mime.setter
    def mime(self, value: str):
        """Set MIME of the file
        """
        self.set_field('mime', value)

    def get_url(self, **kwargs) -> str:
        """Get URL of the file
        """
        return self.get_field('url', **kwargs)

    @property
    def url(self) -> str:
        """Shortcut
        """
        return self.get_url()

    def get_thumb_url(self, **kwargs) -> str:
        """Get thumbnail URL of the file
        """
        return self.get_field('thumb_url', **kwargs)

    @property
    def thumb_url(self) -> str:
        """Shortcut
        """
        return self.get_thumb_url()

    def get_field(self, field_name: str, **kwargs) -> _Any:
        # File download URL
        if field_name == 'url':
            return _router.rule_url('file@download', {'uid': self.uid})

        elif field_name == 'thumb_url':
            ext = self.ext.replace('.', '').lower()
            if ext in _EXT_THUMB:
                ext = _EXT_THUMB[ext]

            return _assetman.url('file@thumbs/{}.svg'.format(ext if ext in _THUMBS else 'file'))

        raise NotImplementedError()

    @_abstractmethod
    def set_field(self, field_name: str, value, **kwargs):
        pass

    @_abstractmethod
    def save(self):
        pass

    @_abstractmethod
    def delete(self):
        pass

    def as_jsonable(self, **kwargs) -> dict:
        r = {}
        for k in 'uid', 'name', 'description', 'mime', 'length', 'url', 'thumb_url':
            try:
                r[k] = self.get_field(k, **kwargs)
            except NotImplementedError:
                pass

        return r


class AbstractImage(AbstractFile):
    @property
    def width(self) -> int:
        """Get width of the image.
        """
        return self.get_field('width')

    @width.setter
    def width(self, value: int):
        """Set width of the image.
        """
        self.set_field('width', value)

    @property
    def height(self) -> int:
        """Get height of the image.
        """
        return self.get_field('height')

    @height.setter
    def height(self, value: int):
        """Set height of the image.
        """
        self.set_field('height', value)

    @property
    def exif(self) -> dict:
        """Get EXIF data of the image.
        """
        return self.get_field('exif')

    @exif.setter
    def exif(self, value: dict):
        """Set EXIF of the image.
        """
        self.set_field('exif', value)

    def get_html(self, alt: str = '', css: str = '', width: int = 0, height: int = 0, enlarge: bool = True):
        """Get HTML code to embed the image.
        """
        if not enlarge:
            if width and width > self.width:
                width = self.width
            if height and height > self.height:
                height = self.height

        css += ' img-responsive'

        return '<img src="{}" class="{}" alt="{}">'.format(
            self.get_url(width=width, height=height), css.strip(), _util.escape_html(alt)
        )

    def get_responsive_html(self, alt: str = '', css: str = '', aspect_ratio: float = None,
                            enlarge: bool = True) -> str:
        """Get HTML code to embed the image (responsive way).
        """
        alt = _util.escape_html(alt)
        css += ' img-responsive img-fluid pytsite-img'

        return '<span class="{}" data-url="{}" data-alt="{}" data-aspect-ratio="{}" ' \
               'data-width="{}" data-height="{}" data-enlarge="{}"></span>' \
            .format(css.strip(), self.url, alt, aspect_ratio, self.width, self.height, enlarge)

    def as_jsonable(self, **kwargs) -> dict:
        r = super().as_jsonable(**kwargs)

        r.update({
            'width': self.width,
            'height': self.height,
        })

        return r
