#-*- coding: utf-8 -*-
import atexit

from selenium.common.exceptions import WebDriverException

from src import consts
from src.crawler import search_board, open_browser, clear_blocked_list, block_user, search_board_from
from src.signin import ensure_signin
from src.utils import console

if __name__ == '__main__':
    def _block(_driver, _board, _no):
        clear_blocked_list(_driver)
        block_user(_driver, _board, _no)

    while True:
        try:
            driver = open_browser(consts.DRIVER_PATH)
            atexit.register(lambda: driver.quit())

            ensure_signin(driver)

            board = "ob"
            no = "167195"
            _block(driver, board, no)
            ## Search author of <site_url>/bbs/view.php?id=mento&no=1423661
            # search_board(driver, "mento", "1423661")

            ## Search author of <site_url>/bbs/view.php?id=ob&no=167039, in latest 100 articles.
            search_board_from(driver, board, no, 167300)
        except WebDriverException as e:
            console.error(e)
