#-*- coding: utf-8 -*-
import atexit

from selenium.common.exceptions import WebDriverException

from src import consts
from src.crawler import search_board, open_browser, search_board_from, clear_blocked_list, block_user
from src.signin import ensure_signin
from src.utils import console

if __name__ == '__main__':
    def _block(_driver, _board, _no):
        clear_blocked_list(_driver)
        block_user(_driver, _board, _no)

    driver = open_browser(consts.DRIVER_PATH)
    atexit.register(lambda: driver.quit())

    ensure_signin(driver)
    board = "pegasusb_a2157"
    no = "8959"
    _block(driver, board, no)
