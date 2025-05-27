"""
This module is used to do a kind of urmidentary logging...
Thie idea behind it is to update the user and the app itself
rather stopping on problems, and allow for decission making

Classes:

    Colors
    Status
"""

from typing import Any
from enum import Enum


class LogLevel(Enum):
    """This enum class is used to determine which color is used for logging"""

    OK = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    SUCCESS = 4
    NOTICE = 5


class Logger:
    """This is a kind of logger object"""

    def __init__(self, level: LogLevel = LogLevel.OK, message: str = "nil") -> None:
        """
        Instanciation of the status object
        """
        self.status: dict[LogLevel, str] = [level, message]
        self.colors: dict[int, str] = {
            0: "\033[0m",
            1: "\033[91m",
            2: "\033[33m",
            3: "\033[94m",
            4: "\033[92m",
            5: "\03[1m",
        }

    def get_log(self) -> str:
        """
        Actually returning the log string
        """
        output: str = ""
        match self.status[0]:
            case LogLevel.ERROR:
                output = f"{self.colors[1]}Error:{self.colors[0]} {self.status[1]}"
            case LogLevel.WARNING:
                output = f"{self.colors[2]}Warning:{self.colors[0]} {self.status[1]}"
            case LogLevel.INFO:
                output = f"{self.colors[3]}Info:{self.colors[0]} {self.status[1]}"
            case LogLevel.SUCCESS:
                output = f"{self.colors[4]}Success:{self.colors[0]} {self.status[1]}"
            case _:
                output = f"{self.colors[5]}Notice:{self.colors[0]} {self.status[1]}"

        return output

    def set_log(self, level: LogLevel, message: str) -> bool:
        """
        Update the status

            Parameters:
                level (LogLevel)
                message (str) the loggin message
        """
        if level.value in range(0, 6):
            self.status[0] = level
            self.status[1] = message
            return True
        self.status[0] = LogLevel.NOTICE
        self.status[1] = "wrong LogLevel"
        return False

    def get_level(sef) -> LogLevel:
        """
        Return the current status level

            Returns:
                the status level (LogLevel)
        """
        return self.status[0]
