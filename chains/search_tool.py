"""Web search tool: SerpAPI (Google) when SERP_API_KEY is set, else DuckDuckGo (free, no key)."""
import os

import requests
from ddgs import DDGS


def _serpapi(query: str, num: int, key: str) -> list:
    resp = requests.get(
        "https://serpapi.com/search.json",
        params={"q": query, "api_key": key, "num": num, "engine": "google"},
        timeout=30,
    )
    resp.raise_for_status()
    return [
        {"title": r.get("title", ""), "url": r.get("link", ""), "text": r.get("snippet", "")}
        for r in resp.json().get("organic_results", [])[:num]
    ]


def _ddg(query: str, num: int) -> list:
    return [
        {"title": r.get("title", ""), "url": r.get("href", ""), "text": r.get("body", "")}
        for r in DDGS().text(query, max_results=num)
    ]


def web_search(query: str, num: int = 8) -> str:
    """Return search results formatted as numbered text with source URLs."""
    key = os.getenv("SERP_API_KEY")
    results = []
    if key:
        try:
            results = _serpapi(query, num, key)
        except requests.RequestException:
            pass  # fall back to DuckDuckGo
    if not results:
        results = _ddg(query, num)
    if not results:
        return "No search results found."
    return "\n\n".join(
        f"[{i}] {r['title']}\nURL: {r['url']}\n{r['text']}" for i, r in enumerate(results, 1)
    )
