from enum import IntEnum

class TaskStatus(IntEnum):
    NOT_STARTED = 0
    DOING = 1
    FAILED = 2
    SUCCESS = 3