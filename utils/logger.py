from colorama import Fore
from utils.types import LogType


class Logger:
    def log(self, type: LogType, message):
        if type == LogType.ERROR:
            print(Fore.RED, message)
        elif type == LogType.INFO:
            print(Fore.GREEN, message)
        elif type == LogType.WARNING:
            print(Fore.YELLOW, message)
