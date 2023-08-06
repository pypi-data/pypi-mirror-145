"""STTP package root."""

from . import errors
from . import ext
from . import subst
from . import pkg_meta
from . import core

from .parser import Parser

__version__ = pkg_meta.version

__all__ = [
    'Parser',
    'errors',
    'ext',
    'subst',
    'pkg_meta',
    'core',
]
