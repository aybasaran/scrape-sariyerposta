from colorama import Fore
from utils.types import LogType


class Logger:
    def log(self, type: LogType, message):
        if type == LogType.ERROR:
            print(Fore.RED, message)
            # reset colorama
        elif type == LogType.SUCCESS:
            print(Fore.GREEN, message)
        elif type == LogType.WARNING:
            print(Fore.YELLOW, message)
        elif type == LogType.INFO:
            print(Fore.BLUE, message)

        print(Fore.RESET)
