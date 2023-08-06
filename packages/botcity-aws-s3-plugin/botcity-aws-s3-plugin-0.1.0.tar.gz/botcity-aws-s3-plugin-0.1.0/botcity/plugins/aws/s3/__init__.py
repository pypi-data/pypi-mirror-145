from .plugin import BotAWSS3Plugin  # noqa: F401, F403
from .filter import Filter  # noqa: F401, F403

from . import _version
__version__ = _version.get_versions()['version']
