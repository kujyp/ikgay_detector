import os

from src.config import SITE_HOST

COOKIE_PATH = os.path.join("data", "cookie.json")
DRIVER_PATH = os.path.join("driver", "chromedriver")
SITE_HOST_WITHOUT_TRAILING_SLASH = SITE_HOST.rstrip('/')
SIGNIN_ID_ELEMENT_NAME = "user_id"
SIGNIN_PW_ELEMENT_NAME = "password"
