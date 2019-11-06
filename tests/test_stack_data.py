from src import consts, stack_data


def test_get_article_num_from_url():
    assert stack_data.get_article_num_from_url("https://www.koreapas.com/bbs/view.php?id=ob&page=1&sn1=&divpage=33&sn=off&ss=on&sc=on&select_arrange=headnum&desc=asc&no=169969") == 169969
    assert stack_data.get_article_num_from_url("https://www.koreapas.com/bbs/view.php?id=ob&page=1&sn1=&no=169969&divpage=33") == 169969
