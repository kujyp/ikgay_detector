#-*- coding: utf-8 -*-
import atexit

from selenium.common.exceptions import WebDriverException

from src import consts
from src.crawler import search_board, open_browser, search_board_from
from src.signin import ensure_signin
from src.utils import console

if __name__ == '__main__':
    while True:
        try:
            driver = open_browser(consts.DRIVER_PATH)
            atexit.register(lambda: driver.quit())

            ensure_signin(driver)

            ## Search author of <site_url>/bbs/view.php?id=mento&no=1423661
            # search_board(driver, "mento", "1423661")

            ## Search author of <site_url>/bbs/view.php?id=ob&no=167039, in latest 100 articles.
            searched = search_board_from(driver, "pegasusb_a2157", "8959", from_num=5250, to_num=5500)
            if searched:
                break
        except WebDriverException as e:
            console.error(e)
