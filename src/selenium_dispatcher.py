from random import random, randint
import time

from src.utils import console


MAXDELAY_IN_SECONDS = 0.5


def random_delay():
    seconds = random() * (MAXDELAY_IN_SECONDS / 16)
    if randint(0, 1) == 1:
        seconds += random() * (MAXDELAY_IN_SECONDS / 8)

        if randint(0, 1) == 1:
            seconds += random() * (MAXDELAY_IN_SECONDS / 4)

            if randint(0, 1) == 1:
                seconds += random() * (MAXDELAY_IN_SECONDS / 2)

    time.sleep(seconds)


def driver_get(driver, url):
    random_delay()
    driver.get(url)


def element_send_key(element, k):
    random_delay()
    element.send_keys(k)


def element_click(element):
    random_delay()
    element.click()


def accept_alert(driver):
    alert = driver.switch_to.alert
    console.info(f"alert=[{alert.text}]")
    alert.accept()
