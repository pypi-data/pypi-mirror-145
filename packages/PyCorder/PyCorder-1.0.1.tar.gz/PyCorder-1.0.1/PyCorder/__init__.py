from .manager import install
install()

from .record import MicRecorder, MicStream

__version__ = '1.0.1'
__all__ = (
    'MicRecorder', 'MicStream', '__version__',
)