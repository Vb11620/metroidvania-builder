from colorama import Fore


## Logs


def log(message: str):
    print(f">> {message}")


def minor_log(message: str):
    print(message)


def critical_error(error: str):
    exit(f"{Fore.RED}>> Error: {error}{Fore.RESET}")


def achievement_log(message: str):
    print(f"{Fore.GREEN}>> {message}{Fore.RESET}")
