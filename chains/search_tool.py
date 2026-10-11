"""Web search tool (DuckDuckGo, free, no API key)."""
from ddgs import DDGS


def web_search(query: str, num: int = 8) -> str:
    """Return search results formatted as numbered text with source URLs."""
    results = DDGS().text(query, max_results=num)
    if not results:
        return "No search results found."
    return "\n\n".join(
        f"[{i}] {r.get('title', '')}\nURL: {r.get('href', '')}\n{r.get('body', '')}"
        for i, r in enumerate(results, 1)
    )
