"""
dtu_conf: <DESCRIPTION>
"""
import logging

from ._version import version as __version__
from .DTU_config import DtuConfig as DtuConfig

logging.getLogger(__name__).addHandler(logging.NullHandler())
