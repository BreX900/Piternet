import platform
from enum import Enum


class System(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"


system = System(platform.system())

