
import json
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser


class BaseCrawler(ABC):
    def __init__(
        self,
        base_url: str,
        source_name: str,
        delay: float = 3.0,
        timeout: int = 15,
    ):
        self.base_url = base_url.rstrip("/")
        self.source_name = source_name
        self.delay = delay
        self.timeout = timeout
        self.last_request_time = 0.0
        self.robots_checked = False
        self.robots_parser = RobotFileParser()

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "StockMarketResearchBot/1.0"
        })

    def _check_robots(self):
        """Load robots.txt once. Fail closed if its rules cannot be checked."""
        if self.robots_checked:
            return

        robots_url = urljoin(self.base_url + "/", "robots.txt")

        try:
            response = self.session.get(
                robots_url,
                timeout=self.timeout
            )

            if response.status_code == 404:
                self.robots_parser.parse([])
            else:
                response.raise_for_status()
                self.robots_parser.parse(response.text.splitlines())

            self.robots_checked = True

        except requests.RequestException as exc:
            raise RuntimeError(
                f"Could not verify robots.txt for {self.source_name}: {exc}"
            ) from exc

    def _request(self, url: str):
        """Fetch a URL only if robots.txt permits it."""
        self._check_robots()

        if not self.robots_parser.can_fetch(
            self.session.headers["User-Agent"],
            url
        ):
            raise PermissionError(
                f"robots.txt disallows this URL: {url}"
            )

        elapsed = time.monotonic() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        response = self.session.get(
            url,
            timeout=self.timeout
        )
        response.raise_for_status()

        self.last_request_time = time.monotonic()
        return response

    def _get_soup(self, url: str):
        response = self._request(url)
        return BeautifulSoup(response.text, "html.parser")

    @staticmethod
    def _meta_content(soup, *selectors):
        for selector in selectors:
            tag = soup.select_one(selector)
            if tag:
                value = tag.get("content") or tag.get_text(" ", strip=True)
                if value:
                    return value.strip()
        return None

    @staticmethod
    def _extract_json_ld(soup):
        """Find NewsArticle metadata in JSON-LD, if the page provides it."""
        for script in soup.select(
            'script[type="application/ld+json"]'
        ):
            try:
                data = json.loads(script.string or script.get_text())
            except (json.JSONDecodeError, TypeError):
                continue

            objects = data if isinstance(data, list) else [data]

            for obj in objects:
                if not isinstance(obj, dict):
                    continue

                if "@graph" in obj and isinstance(obj["@graph"], list):
                    objects.extend(obj["@graph"])

                obj_type = obj.get("@type", "")
                if isinstance(obj_type, list):
                    obj_type = " ".join(obj_type)

                if any(
                    item in str(obj_type)
                    for item in ("NewsArticle", "Article", "BlogPosting")
                ):
                    return obj

        return {}

    @staticmethod
    def _parse_date(value):
        if not value:
            return None

        try:
            parsed = date_parser.parse(str(value))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed
        except (ValueError, TypeError, OverflowError):
            try:
                parsed = parsedate_to_datetime(str(value))
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                return parsed
            except (ValueError, TypeError, OverflowError):
                return None

    def extract_article_metadata(self, url: str):
        soup = self._get_soup(url)
        json_ld = self._extract_json_ld(soup)

        headline = (
            json_ld.get("headline")
            or self._meta_content(
                soup,
                'meta[property="og:title"]',
                'meta[name="twitter:title"]',
            )
        )

        if not headline:
            h1 = soup.find("h1")
            headline = h1.get_text(" ", strip=True) if h1 else None

        description = (
            json_ld.get("description")
            or self._meta_content(
                soup,
                'meta[property="og:description"]',
                'meta[name="description"]',
                'meta[name="twitter:description"]',
            )
        )

        published_value = (
            json_ld.get("datePublished")
            or self._meta_content(
                soup,
                'meta[property="article:published_time"]',
                'meta[name="datePublished"]',
                "time[datetime]",
            )
        )

        canonical = soup.find("link", rel="canonical")
        canonical_url = (
            urljoin(url, canonical.get("href"))
            if canonical and canonical.get("href")
            else url
        )

        return {
            "headline": headline.strip() if headline else None,
            # Keep a short description, not the full copyrighted article.
            "body": description[:500] if description else None,
            "source": self.source_name,
            "url": canonical_url,
            "published_at": self._parse_date(published_value),
        }

    @abstractmethod
    def crawl(self, max_articles: int = 10):
        """Return a list of article metadata dictionaries."""
        raise NotImplementedError

    def close(self):
        self.session.close()
