import os

from src.config import SITE_HOST

COOKIE_PATH = os.path.join("data", "cookie.json")
DRIVER_PATH = os.path.join("driver", "chromedriver")


def ensure_starts_with_www(url):
    prefix = ""
    if url.startswith("http://"):
        prefix = "http://"
    elif url.startswith("https://"):
        prefix = "https://"

    url_without_prefix = url[len(prefix):]
    if not url_without_prefix.startswith("www."):
        url_without_prefix = "www." + url_without_prefix
    return prefix + url_without_prefix


SITE_HOST_WITHOUT_TRAILING_SLASH = ensure_starts_with_www(SITE_HOST.rstrip('/'))
SIGNIN_ID_ELEMENT_NAME = "user_id"
SIGNIN_PW_ELEMENT_NAME = "password"
