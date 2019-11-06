

class Article():
    def __init__(self) -> None:
        super().__init__()
        self.board = None

        self.comment_count = -1
        self.created_at = None
        self.topic = None

        self.nickname = None
        self.url = None

        self.article_num = -1
        self.title = None
        self.crawled_list_at = None

        # self.crawled_detail_at = None

    def set_by_list_page(self,
                         board,
                         comment_count, created_at,
                         nickname, url, article_num,
                         title, crawled_list_at):
        self.board = board
        self.comment_count = comment_count
        self.created_at = created_at

        self.nickname = nickname
        self.url = url
        self.article_num = article_num

        self.title = title
        self.crawled_list_at = crawled_list_at
