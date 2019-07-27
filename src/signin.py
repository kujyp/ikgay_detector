import os
import pickle

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from src import consts, selenium_dispatcher
from src.config import MY_ACCOUNT, MY_PASSWORD
from src.utils import fileio, console


def save_cookie(driver, path):
    console.info()
    fileio.make_parent_path_if_doesnt_exist(path)
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


def load_cookie_if_exists(driver, path):
    console.info()
    if not os.path.exists(path):
        return

    with open(path, 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)


def signin(driver):
    console.info()
    selenium_dispatcher.driver_get(driver, consts.SITE_HOST_WITHOUT_TRAILING_SLASH)
    elements_id = driver.find_element_by_name(consts.SIGNIN_ID_ELEMENT_NAME)
    elements_pw = driver.find_element_by_name(consts.SIGNIN_PW_ELEMENT_NAME)

    elements_id.send_keys(MY_ACCOUNT)
    elements_pw.send_keys(MY_PASSWORD)
    selenium_dispatcher.element_send_key(elements_pw, Keys.ENTER)


def is_signed_in(driver):
    console.info()
    selenium_dispatcher.driver_get(driver, consts.SITE_HOST_WITHOUT_TRAILING_SLASH)
    try:
        driver.find_element_by_name(consts.SIGNIN_ID_ELEMENT_NAME)
        return False
    except NoSuchElementException:
        return True


def ensure_signin(driver):
    console.info()
    if not is_signed_in(driver):
        load_cookie_if_exists(driver, consts.COOKIE_PATH)

    if not is_signed_in(driver):
        signin(driver)
        save_cookie(driver, consts.COOKIE_PATH)
