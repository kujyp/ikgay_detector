#-*- coding: utf-8 -*-
import atexit

from src import consts
from src.crawler import search_board, open_browser
from src.signin import ensure_signin


if __name__ == '__main__':
    driver = open_browser(consts.DRIVER_PATH)
    atexit.register(lambda: driver.quit())

    ensure_signin(driver)

    ## Search author of <site_url>/bbs/view.php?id=mento&no=1423661
    # search_board(driver, "mento", "1423661")

    ## Search author of <site_url>/bbs/view.php?id=ob&no=167039, in latest 100 articles.
    search_board(driver, "ob", "167039", 100)
