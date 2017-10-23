from enum import Enum


class PASS_DIRECTION(Enum):
    LEFT = 1
    RIGHT = -1
    ACROSS = 2
    NO_PASS = 0