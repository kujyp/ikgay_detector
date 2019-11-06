from src import consts


def test_ensure_starts_with_www():
    assert consts.ensure_starts_with_www("http://naver.com") == "http://www.naver.com"
    assert consts.ensure_starts_with_www("https://naver.com") == "https://www.naver.com"
    assert consts.ensure_starts_with_www("http://www.naver.com") == "http://www.naver.com"
    assert consts.ensure_starts_with_www("https://www.naver.com") == "https://www.naver.com"
