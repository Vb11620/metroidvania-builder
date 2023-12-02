from colorama import Fore


## Logs


def log(message):
    print(f">> {message}")


def minor_log(message):
    print(message)


def critical_error(error):
    exit(f"{Fore.RED}>> Error: {error}{Fore.RESET}")


def achievement_log(message):
    print(f"{Fore.GREEN}>> {message}{Fore.RESET}")
