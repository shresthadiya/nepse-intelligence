from sqlalchemy.orm import Session

from app.models.news import News

from app.crawlers.sharesansar import SharesansarCrawler
from app.crawlers.merolagani import MerolaganiCrawler
from app.crawlers.bizmandu import BizmanduCrawler
from app.crawlers.nepselapha import NepseAlphaCrawler

from app.services.categorization.categorizer import (
    categorize_news
)


def run_crawler(
    db: Session,
    crawler_class,
    max_articles: int = 10
):
    """Run a crawler, save articles and categorize them."""

    crawler = crawler_class()
    source = crawler.source_name

    result = {
        "source": source,
        "fetched": 0,
        "inserted": 0,
        "duplicates": 0,
        "categorized": 0,
        "uncategorized": 0,
        "failed": 0
    }

    try:
        articles = crawler.crawl(
            max_articles=max_articles
        )

        result["fetched"] = len(articles)

        article_urls = {
            article.get("url")
            for article in articles
            if article.get("url")
        }

        existing_urls = {
            row[0]
            for row in db.query(News.url)
            .filter(News.url.in_(article_urls))
            .all()
        } if article_urls else set()

        seen_urls = set()

        for article in articles:

            url = article.get("url")

            if not url:
                result["failed"] += 1
                continue

            if url in existing_urls or url in seen_urls:
                result["duplicates"] += 1
                continue

            seen_urls.add(url)

            news = News(
                headline=article["headline"],
                body=article.get("body", ""),
                source=article.get("source", source),
                url=url,
                published_at=article.get("published_at")
            )

            db.add(news)

            # Generate the news ID.
            db.flush()

            # Automatically categorize the article.
            categorization = categorize_news(
                db=db,
                news=news
            )

            result["inserted"] += 1

            if categorization["total_matches"] > 0:
                result["categorized"] += 1
            else:
                result["uncategorized"] += 1

        db.commit()

        print(
            f"{source}: "
            f"{result['inserted']} inserted, "
            f"{result['duplicates']} duplicates, "
            f"{result['categorized']} categorized"
        )

    except Exception as exc:

        db.rollback()

        result["failed"] += 1

        print(f"{source} crawler failed: {exc}")

        raise

    finally:
        crawler.close()

    return result


def run_all_crawlers(
    db: Session,
    max_articles: int = 10
):
    """Execute all registered crawlers."""

    crawlers = [
        SharesansarCrawler,
        MerolaganiCrawler,
        BizmanduCrawler,
        NepseAlphaCrawler
    ]

    results = []

    for crawler_class in crawlers:

        try:
            result = run_crawler(
                db=db,
                crawler_class=crawler_class,
                max_articles=max_articles
            )

            results.append(result)

        except Exception as exc:

            results.append({
                "source": crawler_class.__name__,
                "fetched": 0,
                "inserted": 0,
                "duplicates": 0,
                "categorized": 0,
                "uncategorized": 0,
                "failed": 1,
                "error": str(exc)
            })

    return results