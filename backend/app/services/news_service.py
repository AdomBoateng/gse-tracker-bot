import asyncio
import hashlib
import json
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from typing import Any, Dict, List
from urllib.parse import quote_plus, urljoin

import httpx
from sqlalchemy.orm import Session

from app.db import crud
from app.db.session import SessionLocal

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
CACHE_TTL_SECONDS = 300
MAX_ARTICLES = 80
MAX_FETCHED_QUERIES = 40
REFRESH_INTERVAL_SECONDS = 30 * 60


class LinkExtractor(HTMLParser):
    """Small anchor extractor for official pages without adding parser deps."""

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.links: List[Dict[str, str]] = []
        self._href: str | None = None
        self._text_parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attrs_dict = dict(attrs)
        href = attrs_dict.get("href")
        if href:
            self._href = urljoin(self.base_url, href)
            self._text_parts = []

    def handle_data(self, data: str) -> None:
        if self._href:
            self._text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or not self._href:
            return
        title = " ".join(" ".join(self._text_parts).split())
        if title and len(title) >= 8:
            self.links.append({"title": title, "url": self._href})
        self._href = None
        self._text_parts = []


class NewsService:
    """Persist stock news from official pages and public Google News RSS."""

    def __init__(self):
        self._cache: Dict[str, Any] | None = None
        self._cache_time = 0.0
        self._last_refresh_time = 0.0
        self._refresh_lock = asyncio.Lock()

    @staticmethod
    def _url_hash(url: str) -> str:
        return hashlib.sha256(url.strip().lower().encode("utf-8")).hexdigest()

    @staticmethod
    def _today() -> str:
        return datetime.now(timezone.utc).date().isoformat()

    @staticmethod
    def _format_date(value: str | None) -> str:
        if not value:
            return ""
        try:
            return parsedate_to_datetime(value).date().isoformat()
        except (TypeError, ValueError):
            return value

    @staticmethod
    def _clean_title(title: str) -> str:
        return " ".join(title.replace("\n", " ").split())

    @staticmethod
    def _source_from_item(item: ET.Element) -> str:
        source = item.find("source")
        if source is not None and source.text:
            return source.text.strip()
        return "Google News"

    @staticmethod
    def _classify(title: str, topic: str = "") -> str:
        text = f"{title} {topic}".lower()
        if "dividend" in text:
            return "Dividends"
        if "ipo" in text or "initial public offering" in text or "listing" in text:
            return "IPO"
        if "annual report" in text or "financial statement" in text or "results" in text:
            return "Financials"
        if "announcement" in text or "disclosure" in text or "notice" in text:
            return "Official"
        return "Company News"

    @staticmethod
    def _listed_companies() -> List[Dict[str, str]]:
        path = os.path.join(BACKEND_DIR, "stocks.txt")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"stocks": []}

        seen = set()
        companies = []
        for stock in data.get("stocks", []):
            symbol = str(stock.get("symbol", "")).strip().upper()
            company_name = str(stock.get("company_name", symbol)).strip()
            if not symbol or symbol in seen:
                continue
            seen.add(symbol)
            companies.append({"symbol": symbol, "company_name": company_name})
        return companies

    @staticmethod
    def _official_sources() -> List[Dict[str, str]]:
        path = os.path.join(DATA_DIR, "news_sources.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return []
        return data.get("sources", [])

    def _market_links(self) -> List[Dict[str, Any]]:
        links = [
            {
                "title": "Ghana Stock Exchange market announcements",
                "url": "https://gse.com.gh/news-announcements/",
                "source": "Ghana Stock Exchange",
                "topic": "Official market announcements",
                "category": "Official",
            },
            {
                "title": "Ghana Stock Exchange listed company disclosures",
                "url": "https://gse.com.gh/listed-companies/",
                "source": "Ghana Stock Exchange",
                "topic": "Listed company information",
                "category": "Official",
            },
            {
                "title": "Ghana Stock Exchange news and updates",
                "url": "https://gse.com.gh/news/",
                "source": "Ghana Stock Exchange",
                "topic": "Exchange news",
                "category": "Company News",
            },
        ]
        return [
            self._normalize_item({**link, "source_type": "official", "symbol": None})
            for link in links
        ]

    def _stock_discovery_links(self) -> List[Dict[str, Any]]:
        items = []
        for stock in self._listed_companies():
            symbol = stock["symbol"]
            company_name = stock["company_name"]
            query = quote_plus(f'"{company_name}" OR {symbol} Ghana stock dividend IPO')
            url = f"https://news.google.com/search?q={query}&hl=en-GH&gl=GH&ceid=GH:en"
            items.append(
                self._normalize_item(
                    {
                        "symbol": symbol,
                        "company_name": company_name,
                        "title": f"Latest {symbol} news and filings",
                        "url": url,
                        "source": "Google News",
                        "source_type": "search",
                        "category": "Company News",
                        "topic": f"{company_name} company news",
                        "summary": (
                            f"Search link for public news, dividends, IPO updates, "
                            f"and company filings related to {company_name}."
                        ),
                    }
                )
            )
        return items

    def _normalize_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        title = self._clean_title(str(item.get("title", "")))
        url = str(item.get("url", "")).strip()
        topic = str(item.get("topic", "Company News"))
        category = str(item.get("category") or self._classify(title, topic))
        return {
            "symbol": item.get("symbol"),
            "company_name": item.get("company_name"),
            "title": title,
            "url": url,
            "url_hash": self._url_hash(url),
            "published_at": item.get("published_at") or self._today(),
            "source": item.get("source") or "Public source",
            "source_type": item.get("source_type") or "media",
            "category": category,
            "topic": topic,
            "summary": item.get("summary") or "",
        }

    def _topic_queries(self) -> List[Dict[str, str]]:
        market_terms = [
            {"query": '"Ghana Stock Exchange" IPO', "symbol": "", "company_name": ""},
            {"query": '"Ghana Stock Exchange" dividends', "symbol": "", "company_name": ""},
            {"query": '"Ghana Stock Exchange" listed company', "symbol": "", "company_name": ""},
            {"query": '"GSE" market announcement Ghana', "symbol": "", "company_name": ""},
        ]
        company_terms = [
            {
                "query": f'"{stock["company_name"]}" OR {stock["symbol"]}',
                "symbol": stock["symbol"],
                "company_name": stock["company_name"],
            }
            for stock in self._listed_companies()
        ]
        return (market_terms + company_terms)[:MAX_FETCHED_QUERIES]

    async def _fetch_google_query(
        self,
        client: httpx.AsyncClient,
        query_item: Dict[str, str],
    ) -> List[Dict[str, Any]]:
        encoded = quote_plus(f"{query_item['query']} Ghana stock")
        url = (
            "https://news.google.com/rss/search"
            f"?q={encoded}&hl=en-GH&gl=GH&ceid=GH:en"
        )
        try:
            response = await client.get(url, timeout=20.0, follow_redirects=True)
            response.raise_for_status()
            root = ET.fromstring(response.text)
        except (httpx.HTTPError, ET.ParseError) as error:
            print(f"Error fetching Google News for {query_item['query']}: {error}")
            return []

        articles = []
        for item in root.findall("./channel/item"):
            title = self._clean_title(item.findtext("title", ""))
            link = item.findtext("link", "")
            if not title or not link:
                continue
            articles.append(
                self._normalize_item(
                    {
                        "symbol": query_item.get("symbol") or None,
                        "company_name": query_item.get("company_name") or None,
                        "title": title,
                        "url": link,
                        "published_at": self._format_date(item.findtext("pubDate")),
                        "source": self._source_from_item(item),
                        "source_type": "media",
                        "topic": query_item["query"].replace('"', ""),
                    }
                )
            )
        return articles

    async def _scrape_official_source(
        self,
        client: httpx.AsyncClient,
        source: Dict[str, str],
    ) -> List[Dict[str, Any]]:
        url = source.get("url", "")
        if not url:
            return []
        try:
            response = await client.get(url, timeout=20.0, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPError as error:
            print(f"Error scraping official source {url}: {error}")
            return []

        parser = LinkExtractor(url)
        parser.feed(response.text)
        items = []
        for link in parser.links[:20]:
            title = link["title"]
            if not any(
                word in title.lower()
                for word in ["news", "announcement", "dividend", "report", "notice", "ipo", "results"]
            ):
                continue
            items.append(
                self._normalize_item(
                    {
                        "symbol": source.get("symbol") or None,
                        "company_name": source.get("company_name") or None,
                        "title": title,
                        "url": link["url"],
                        "source": source.get("source", "Official source"),
                        "source_type": "official",
                        "topic": source.get("topic", "Official company update"),
                    }
                )
            )
        return items

    async def refresh_news(self, db: Session) -> int:
        async with self._refresh_lock:
            items = self._market_links() + self._stock_discovery_links()
            async with httpx.AsyncClient(
                headers={"User-Agent": "gse-tracker-bot/1.0"}
            ) as client:
                for source in self._official_sources():
                    items.extend(await self._scrape_official_source(client, source))
                for query in self._topic_queries():
                    items.extend(await self._fetch_google_query(client, query))

            inserted = crud.upsert_news_items(db, items)
            self._cache = None
            self._last_refresh_time = time.monotonic()
            return inserted

    async def maybe_refresh_news(self, db: Session) -> None:
        if (time.monotonic() - self._last_refresh_time) < CACHE_TTL_SECONDS:
            return
        await self.refresh_news(db)

    async def periodic_refresh(self) -> None:
        while True:
            await asyncio.sleep(REFRESH_INTERVAL_SECONDS)
            db = SessionLocal()
            try:
                await self.refresh_news(db)
            finally:
                db.close()

    async def get_news(
        self,
        db: Session,
        symbol: str | None = None,
        source_type: str | None = None,
        category: str | None = None,
        refresh: bool = False,
    ) -> Dict[str, Any]:
        if refresh:
            await self.refresh_news(db)
        else:
            await self.maybe_refresh_news(db)

        cache_key = f"{symbol or ''}:{source_type or ''}:{category or ''}"
        now = time.monotonic()
        if (
            self._cache is not None
            and self._cache.get("key") == cache_key
            and (now - self._cache_time) < CACHE_TTL_SECONDS
        ):
            return self._cache["payload"]

        rows = crud.get_news_items(
            db,
            limit=MAX_ARTICLES,
            symbol=symbol,
            source_type=source_type,
            category=category,
        )
        payload = {
            "articles": [
                {
                    "symbol": row.symbol,
                    "company_name": row.company_name,
                    "title": row.title,
                    "url": row.url,
                    "published_at": row.published_at or "",
                    "source": row.source,
                    "source_type": row.source_type,
                    "category": row.category,
                    "topic": row.topic,
                    "summary": row.summary or "",
                }
                for row in rows
            ],
            "disclaimer": (
                "News links are aggregated from official pages and public search feeds. "
                "Verify market-sensitive items with official company disclosures and the Ghana Stock Exchange."
            ),
        }
        self._cache = {"key": cache_key, "payload": payload}
        self._cache_time = now
        return payload


news_service = NewsService()
