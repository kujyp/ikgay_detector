#-*- coding: utf-8 -*-
import atexit

from selenium.common.exceptions import WebDriverException

from src import consts
from src.crawler import open_browser
from src.signin import ensure_signin
from src.stack_data import crawl_board
from src.utils import console

if __name__ == '__main__':
    try:
        driver = open_browser(consts.DRIVER_PATH)
        atexit.register(lambda: driver.quit())

        ensure_signin(driver)

        crawl_board(driver, "talk2", from_page=1, to_page=5)
    except WebDriverException as e:
        console.error(e)
