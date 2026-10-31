from urllib.parse import urljoin, urlparse

from app.crawlers.base_crawler import BaseCrawler


class SharesansarCrawler(BaseCrawler):

    def __init__(self):
        super().__init__(
            base_url="https://www.sharesansar.com",
            source_name="Sharesansar",
            delay=3.0,
        )

        self.listing_url = (
            "https://www.sharesansar.com/index.php/news-page"
        )

    def get_article_links(self, max_articles=10):
        soup = self._get_soup(self.listing_url)

        links = []
        seen = set()

        for anchor in soup.find_all("a", href=True):
            href = anchor["href"].strip()

            article_url = urljoin(self.base_url, href)
            parsed = urlparse(article_url)

            if parsed.netloc != urlparse(self.base_url).netloc:
                continue

            if "/index.php/newsdetail/" not in parsed.path:
                continue

            if article_url not in seen:
                seen.add(article_url)
                links.append(article_url)

            if len(links) >= max_articles:
                break

        return links

    def crawl(self, max_articles=10):
        articles = []

        links = self.get_article_links(max_articles)

        print(f"Sharesansar: Found {len(links)} article links")

        for article_url in links:
            try:
                article = self.extract_article_metadata(article_url)

                # Always retain the individual article URL.
                article["url"] = article_url
                article["source"] = "Sharesansar"

                if not article.get("headline"):
                    print(
                        f"Skipping article without headline: {article_url}"
                    )
                    continue

                articles.append(article)

            except Exception as exc:
                print(
                    f"Sharesansar article failed: "
                    f"{article_url} - {exc}"
                )

        return articles