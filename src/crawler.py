import os
import random

from selenium import webdriver

from src import download_driver, selenium_dispatcher
from src.utils import console
from src.utils.fileio import save_as_json, \
    load_from_json_or_none
from src.config import SITE_HOST, EACH_POST_RANDOM_SEARCH_COUNT


def get_link_with(board, no):
    return f"{SITE_HOST}/bbs/view.php?id={board}&allc=1&no={no}"


def get_id_nickname_with_link(driver, link):
    selenium_dispatcher.driver_get(driver, link)

    nickname = driver.find_elements_by_xpath("html/body/div/div")[-1] \
        .find_elements_by_xpath("div/table")[1] \
        .find_elements_by_xpath("tbody/tr/td")[1] \
        .find_elements_by_xpath("span")[1].text

    assert nickname is not None
    return nickname


def get_latest_article_no(driver, board):
    selenium_dispatcher.driver_get(driver, f"{SITE_HOST}/bbs/zboard.php?id={board}")
    a_tag_element = driver.find_elements_by_class_name("list_title")[0]\
        .find_element_by_xpath('..')
    link = a_tag_element.get_attribute("href")
    no_idx = link.find("no=")
    no_queries = link[no_idx:]

    other_query_idx_st = no_queries.find("&")
    if other_query_idx_st != -1:
        no_queries = no_queries[:other_query_idx_st]

    article_num = int(no_queries[len("no="):])

    return article_num


def get_article(driver, board, no):
    selenium_dispatcher.driver_get(driver, get_link_with(board, no))


def is_author_blocked_user(driver):
    try:
        block_btn = driver.find_element_by_partial_link_text("차단해제")
        if block_btn.get_attribute("href").find("ban_ex.php") != -1:
            return True
    except BaseException:
        pass

    return False


def get_blocked_reply_num_or_none(driver):
    try:
        reply_btns = driver.find_elements_by_class_name("reply2btn")
        comment_idx = 1
        for idx, btn in enumerate(reply_btns):
            if reply_btns[idx].text.startswith("베스트 댓글 "):
                continue
            if reply_btns[idx].text == "BEST":
                continue
            if reply_btns[idx].text == "논란의 댓글":
                continue

            if reply_btns[idx].text != f"댓글 {comment_idx}":
                console.info(f"[댓글 {comment_idx}] not exists.")
                return comment_idx
            comment_idx += 1
    except BaseException:
        pass

    return None


def clear_blocked_list(driver):
    selenium_dispatcher.driver_get(driver, f"{SITE_HOST}/bbs/member_modify.php?group_no=1")

    btn_list = driver.find_elements_by_class_name("butt_red")
    for each_btn in btn_list:
        onclick = each_btn.get_attribute("onclick")
        if onclick and onclick.startswith("ban_clear"):
            selenium_dispatcher.element_click(each_btn)
            selenium_dispatcher.accept_alert(driver)
            return
    console.info("[Clear block user list button] is disabled. It means you have no block users.")


def block_user(driver, board, no):
    selenium_dispatcher.driver_get(driver, f"{SITE_HOST}/bbs/ban_ik.php?id={board}&no={no}")
    selenium_dispatcher.accept_alert(driver)


def search_board_from(driver, board, no, from_num, to_num=0, max_search_post_count=-1):
    data_dirname = f"{board}_{no}"
    data_dirpath = os.path.join("data", data_dirname)
    data_searched_dirpath = os.path.join(data_dirpath, "searched")
    data_found_author_dirpath = os.path.join(data_dirpath, "found_author")
    data_found_replier_dirpath = os.path.join(data_dirpath, "found_replier")

    if from_num < to_num:
        console.warn(f"from_num=[{from_num}] < to_num=[{to_num}]. Swap each value.")
        buff = to_num
        to_num = from_num
        from_num = buff

    console.info(f"Search from article no [{from_num}].")
    no_target = from_num

    idx = 0
    exitflag = False

    while True:
        if exitflag:
            console.info("exit")
            break
        if no_target < to_num or no_target < 0:
            console.notice("Every article has searched.")
            return True

        curr_no_items = list(range(no_target, no_target - EACH_POST_RANDOM_SEARCH_COUNT, -1))
        console.info(f"Search article no [{no_target}] ~ [{no_target - EACH_POST_RANDOM_SEARCH_COUNT}] randomly.")
        random.shuffle(curr_no_items)
        for curr_no in curr_no_items:
            if curr_no < 0 or curr_no < to_num:
                console.info(f"Skip out of range article number. [{curr_no}]")
                continue
            if max_search_post_count != -1 and idx >= max_search_post_count:
                console.notice(f"searched [{max_search_post_count}]")
                exitflag = True
                break

            searched_filepath = os.path.join(data_searched_dirpath, f"{str(curr_no)}")
            found_author_filepath = os.path.join(data_found_author_dirpath, f"{str(curr_no)}.txt")
            found_replier_filepath = os.path.join(data_found_replier_dirpath, f"{str(curr_no)}.txt")
            link = get_link_with(board, curr_no)

            if load_from_json_or_none(searched_filepath) is not None:
                console.info(f"[{searched_filepath}] file exists. skip [{link}]")
                continue
            if load_from_json_or_none(found_author_filepath) is not None:
                console.info(f"[{found_author_filepath}] file exists. skip [{link}]")
                continue
            if load_from_json_or_none(found_replier_filepath) is not None:
                console.info(f"[{found_replier_filepath}] file exists. skip [{link}]")
                continue

            get_article(driver, board, curr_no)
            if is_author_blocked_user(driver):
                console.notice(f"Blocked author found. [{link}]")
                save_as_json(found_author_filepath, link)
            else:
                reply_num = get_blocked_reply_num_or_none(driver)
                if reply_num is not None:
                    console.notice(f"Blocked replier found. [{link}]")
                    save_as_json(found_replier_filepath, {
                        "link": link,
                        "reply_num": reply_num,
                    })
                else:
                    save_as_json(searched_filepath, link)

            idx += 1
        no_target -= EACH_POST_RANDOM_SEARCH_COUNT


# max_search_post_count: -1 == infinity
def search_board(driver, board, no, to_num=0, max_search_post_count=-1):
    console.info()
    latest_no = get_latest_article_no(driver, board)
    console.info(f"Search from article no [{latest_no}](latest).")
    search_board_from(driver, board, no, from_num=latest_no, to_num=to_num, max_search_post_count=max_search_post_count)


def open_browser(driver_path):
    console.info()
    download_driver.install_driver_if_not_installed("driver")

    driver = webdriver.Chrome(driver_path)

    return driver
