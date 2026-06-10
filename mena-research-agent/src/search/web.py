"""Thin search-provider wrapper. Default: Tavily. Swap providers here only —
the rest of the codebase never touches a search API directly.
"""
from __future__ import annotations

import os

import httpx


def search_web(query: str, config) -> list[dict]:
    """Returns [{"url": str, "content": str}]. Empty list on failure."""
    provider = config["search"]["provider"]
    n = config["search"]["results_per_query"]

    if provider == "tavily":
        key = os.environ.get("TAVILY_API_KEY")
        if not key:
            print("  ! TAVILY_API_KEY missing — skipping search")
            return []
        try:
            r = httpx.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": key,
                    "query": query,
                    "max_results": n,
                    "include_raw_content": True,
                },
                timeout=30,
            )
            r.raise_for_status()
            return [
                {"url": hit["url"], "content": hit.get("raw_content") or hit.get("content", "")}
                for hit in r.json().get("results", [])
            ]
        except httpx.HTTPError as e:
            print(f"  ! search failed for '{query}': {e}")
            return []

    raise ValueError(f"Unknown search provider: {provider}")
