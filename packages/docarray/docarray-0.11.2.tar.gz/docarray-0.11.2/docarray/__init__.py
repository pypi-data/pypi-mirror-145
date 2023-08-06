__version__ = '0.11.2'

import os

from .document import Document
from .array import DocumentArray


if 'DA_NO_RICH_HANDLER' not in os.environ:
    from rich.traceback import install

    install()
