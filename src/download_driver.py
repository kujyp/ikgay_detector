import os

from src.utils import fileio, console
from src.utils.shell import get_statement_with_cd, execute_with_message


def download_driver(target_directory):
    fileio.make_path_if_doesnt_exist(target_directory)
    url = "https://chromedriver.storage.googleapis.com/2.43/chromedriver_mac64.zip"
    statement = get_statement_with_cd(target_directory, "wget -O {} {}".format("chromedriver.zip", url))
    execute_with_message(statement)


def extract_driver(target_directory):
    statement = get_statement_with_cd(target_directory, "tar xf {}".format("chromedriver.zip"))
    execute_with_message(statement)


def install_driver(target_directory):
    console.info()
    download_driver(target_directory)
    extract_driver(target_directory)


if __name__ == '__main__':
    install_driver("../driver")


def install_driver_if_not_installed(target_directory):
    chromedriver_path = os.path.join(target_directory, "chromedriver")
    if os.path.exists(chromedriver_path):
        console.info("Driver already installed skip...")
        return

    install_driver(target_directory)
