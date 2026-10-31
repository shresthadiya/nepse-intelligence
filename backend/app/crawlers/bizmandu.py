from app.crawlers.base_crawler import BaseCrawler


class BizmanduCrawler(BaseCrawler):

    def __init__(self):
        super().__init__(
            base_url="https://bizmandu.com",
            source_name="Bizmandu",
            delay=3.0,
        )

        self.listing_url = None

    def crawl(self, max_articles=10):
        raise NotImplementedError(
            "Bizmandu collection requires a verified authorised "
            "news feed or permission-approved data source."
        )