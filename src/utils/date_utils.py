import datetime


def get_today_as_str():
    return get_today().strftime("%Y%m%d")


def get_today():
    return datetime.date.today()
