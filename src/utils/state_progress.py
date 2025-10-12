from enum import Enum


class StateProgress(Enum):
    ERROR = 0
    WARNING = 1
    SUCCESS = 2
    WAITING = 3
    DOWNLOADING = 4
