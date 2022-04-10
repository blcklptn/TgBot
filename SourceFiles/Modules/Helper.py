from colorama import Fore, Style
import zipfile
import os

def logger(message: str = "", log_type: str = "INFO") -> None:
    """ Logger for bot """
    if log_type == "INFO":
        print(f"{Fore.GREEN}[{log_type.upper()}]{Style.RESET_ALL} {message}")
    elif log_type == "WARNING":
        print(f"{Fore.YELLOW}[{log_type.upper()}]{Style.RESET_ALL} {message}")
    elif log_type == "ERROR":
        print(f"{Fore.RED}[{log_type.upper()}]{Style.RESET_ALL} {message}")
    elif log_type == "DEBUG":
        print(f"{Fore.BLUE}[{log_type.upper()}]{Style.RESET_ALL} {message}")
    else:
        print(f"{Fore.MAGENTA}[{log_type.upper()}]{Style.RESET_ALL} {message}")


def unzipper(path, id):
    """ Unzipper for files """
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(f"Sessions/pervonah_data_{id}/")

    os.remove(path)