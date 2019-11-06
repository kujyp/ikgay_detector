import datetime
import os
import time

from src import selenium_dispatcher
from src.consts import SITE_HOST_WITHOUT_TRAILING_SLASH
from src.data import Article
from src.utils import console
from selenium.webdriver.remote.webdriver import WebDriver

from src.utils.fileio import load_article_from_json_or_none, save_as_json

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_article_num_from_url(url):
    from_no_query_url = url[url.find("no="):]
    postfix_removed_url = from_no_query_url
    if from_no_query_url.find('&') != -1:
        postfix_removed_url = from_no_query_url[:from_no_query_url.find('&')]
    return int(postfix_removed_url[len("no="):])


def get_now():
    return datetime.datetime.now()


def str2datetime(strdatetime):
    return datetime.datetime.strptime(strdatetime, DATETIME_FORMAT).date()


def datetime2str(date1):
    return date1.strftime(DATETIME_FORMAT)


def crawl_current_page_articles(driver: WebDriver, board: str, crawled_list_at: str):
    articles = []

    div = driver.find_elements_by_xpath("html/body/div")[0]

    # each_article = div.find_elements_by_css_selector("tr.list0")[0]
    tr_list = []
    tr_list += div.find_elements_by_css_selector("tr.list0")
    tr_list += div.find_elements_by_css_selector("tr.list1")

    for each_article in tr_list:
        comment_count = each_article.find_element_by_css_selector("td.roboto").text
        created_at = each_article.find_element_by_css_selector("nobr").text
        # topic = each_article.find_elements_by_css_selector("td.nanum-g")[0].text
        nickname = each_article.find_elements_by_css_selector("td.nanum-g")[-1].text

        url, article_num, title = None, None, None

        for each_a in each_article.find_elements_by_tag_name('a'):
            article_title_span_list = each_a.find_elements_by_css_selector('span.list_title')
            if not(len(article_title_span_list) > 0):
                continue
            url = each_a.get_property("href")
            article_num = get_article_num_from_url(url)
            title = article_title_span_list[0].text

        assert url is not None
        assert title is not None
        assert article_num is not None
        article = Article()
        article.set_by_list_page(
            board=board,
            comment_count=comment_count,
            created_at=created_at,
            nickname=nickname,
            url=url,
            article_num=article_num,
            title=title,
            crawled_list_at=crawled_list_at,
        )
        articles.append(article)
    return articles


def save_articles(articles):
    # type: (list[Article]) -> None

    if len(articles) == 0:
        return

    board = articles[0].board
    general_path = os.path.join("data", "general", board)
    for article in articles:
        json_path = os.path.join(general_path, str(article.article_num))
        saved_article = load_article_from_json_or_none(json_path)
        if saved_article is None:
            save_as_json(json_path, article)
            continue

        if article.comment_count is not None:
            saved_article.comment_count = article.comment_count
        if article.crawled_list_at is not None:
            saved_article.crawled_list_at = article.crawled_list_at
        if article.title is not None:
            if article.title != saved_article.title:
                saved_article.title = article.title


def crawl_board(driver, board, from_page=1, to_page=10):
    console.info()

    page = from_page

    while True:
        if page > to_page:
            break
        url = f"{SITE_HOST_WITHOUT_TRAILING_SLASH}/bbs/zboard.php?id={board}"
        if page > 1:
            url += f"&page={page}"

        crawled_list_at = datetime2str(get_now())
        selenium_dispatcher.driver_get(driver, url)
        articles = crawl_current_page_articles(driver, board, crawled_list_at)

        save_articles(articles)

        page += 1
