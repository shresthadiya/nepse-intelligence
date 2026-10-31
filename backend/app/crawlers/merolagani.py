from app.crawlers.base_crawler import BaseCrawler


class MerolaganiCrawler(BaseCrawler):

    def __init__(self):
        super().__init__(
            base_url="https://merolagani.com",
            source_name="Merolagani",
            delay=3.0,
        )

        self.listing_url = None

    def crawl(self, max_articles=10):
        raise NotImplementedError(
            "Merolagani collection requires a verified authorised "
            "news feed or permission-approved data source."
        )