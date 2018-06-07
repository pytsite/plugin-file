"""PytSIte File Plugin API Functions
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import os as _os
import magic as _magic
from typing import Optional as _Optional
from urllib.request import urlopen as _urlopen, Request as _urllib_request
from urllib.parse import urlparse as _urlparse
from mimetypes import guess_extension as _guess_extension
from pytsite import reg as _reg, util as _util, validation as _validation
from . import _model, _driver, _error

_current_driver = None


def get_driver() -> _driver.Abstract:
    global _current_driver
    if not _current_driver:
        driver_class = _util.get_module_attr(_reg.get('file.driver', 'plugins.file_storage_odm.Driver'))
        driver = driver_class()

        if not isinstance(driver, _driver.Abstract):
            raise TypeError('Invalid driver instance')

        _current_driver = driver

    return _current_driver


def create(source: str, name: str = None, description: str = None, propose_path: str = None,
           **kwargs) -> _model.AbstractFile:
    """Create a file object from a local or remote file
    """
    # Create temporary file
    tmp_file_d, tmp_file_path = _util.mk_tmp_file()
    tmp_file = open(tmp_file_d, 'wb')

    # Remote file
    try:
        _validation.rule.Url(source).validate()

        # Copy remote file to the temporary local file
        req = _urllib_request(_util.url_quote(source, safe='/:?&%'), headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
        })
        with _urlopen(req) as src:
            data = src.read()
            tmp_file.write(data)

        if not name:
            name = _urlparse(source).path.split('/')[-1]

        if description is None:
            description = 'Downloaded from ' + source

    # Local file
    except _validation.error.RuleError:
        with open(source, 'rb') as f:
            data = f.read()
            tmp_file.write(data)

        if not name:
            name = _os.path.basename(source)

        if description is None:
            description = 'Created from local file ' + source

    # Close temporary file
    tmp_file.close()

    # Validate file's size (in megabytes)
    file_size = _os.stat(tmp_file_path).st_size
    max_file_size_mb = float(_reg.get('file.upload_max_size', '10'))
    if file_size > int(max_file_size_mb * 1048576):
        raise RuntimeError('File size exceeds {} MB'.format(max_file_size_mb))

    # Determining file's MIME type
    mime = _magic.from_file(tmp_file_path, True)

    # Add an extension to the name
    if not _os.path.splitext(name)[1]:
        name += _guess_extension(mime)

    # Ask driver to store file content into its storage
    file_object = get_driver().create(tmp_file_path, mime, name, description, propose_path, **kwargs)

    # Delete temporary file
    _os.unlink(tmp_file_path)

    return file_object


def get(uid: str, suppress_exception: bool = False) -> _Optional[_model.AbstractFile]:
    """Get file
    """
    try:
        return get_driver().get(uid)
    except _error.Error as e:
        if suppress_exception:
            return None

        raise e
