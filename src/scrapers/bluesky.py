"""Bluesky scraper using the public AppView API (no auth required)."""

from __future__ import annotations

import asyncio
from typing import Any

import httpx

API = "https://api.bsky.app/xrpc"
PAGE_SIZE = 100
HEADERS = {"User-Agent": "bluesky-posts-scraper/1.0 (Apify actor)"}


def _post_url(uri: str, handle: str) -> str:
    # at://did:plc:xxx/app.bsky.feed.post/3kabc -> https://bsky.app/profile/handle/post/3kabc
    rkey = uri.rsplit("/", 1)[-1]
    return f"https://bsky.app/profile/{handle}/post/{rkey}"


def _parse_post(post: dict[str, Any], source: str) -> dict[str, Any]:
    author = post.get("author") or {}
    record = post.get("record") or {}
    handle = author.get("handle") or ""
    uri = post.get("uri") or ""
    return {
        "source": source,
        "url": _post_url(uri, handle) if uri and handle else None,
        "text": record.get("text"),
        "authorHandle": handle,
        "authorDisplayName": author.get("displayName"),
        "createdAt": record.get("createdAt"),
        "likeCount": post.get("likeCount", 0),
        "repostCount": post.get("repostCount", 0),
        "replyCount": post.get("replyCount", 0),
        "quoteCount": post.get("quoteCount", 0),
        "langs": record.get("langs") or [],
        "uri": uri,
    }


async def _get(client: httpx.AsyncClient, endpoint: str, params: dict[str, Any]) -> dict[str, Any] | None:
    for attempt in range(3):
        try:
            resp = await client.get(f"{API}/{endpoint}", params=params, headers=HEADERS, timeout=30)
            if resp.status_code == 429:
                await asyncio.sleep(5 * (attempt + 1))
                continue
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError:
            if attempt == 2:
                raise
            await asyncio.sleep(2 * (attempt + 1))
    return None


async def search_posts(
    client: httpx.AsyncClient,
    query: str,
    max_posts: int,
    sort: str = "latest",
    since: str | None = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    cursor: str | None = None
    while len(results) < max_posts:
        params: dict[str, Any] = {
            "q": query,
            "limit": min(PAGE_SIZE, max_posts - len(results)),
            "sort": sort,
        }
        if since:
            params["since"] = f"{since}T00:00:00Z"
        if cursor:
            params["cursor"] = cursor
        data = await _get(client, "app.bsky.feed.searchPosts", params)
        if not data:
            break
        posts = data.get("posts") or []
        if not posts:
            break
        results.extend(_parse_post(p, query) for p in posts)
        cursor = data.get("cursor")
        if not cursor:
            break
    return results[:max_posts]


async def profile_posts(
    client: httpx.AsyncClient,
    handle: str,
    max_posts: int,
    include_replies: bool = False,
    include_reposts: bool = False,
    since: str | None = None,
) -> list[dict[str, Any]]:
    handle = handle.lstrip("@").strip()
    results: list[dict[str, Any]] = []
    cursor: str | None = None
    feed_filter = "posts_with_replies" if include_replies else "posts_no_replies"
    while len(results) < max_posts:
        params: dict[str, Any] = {
            "actor": handle,
            "limit": min(PAGE_SIZE, max_posts - len(results)),
            "filter": feed_filter,
        }
        if cursor:
            params["cursor"] = cursor
        data = await _get(client, "app.bsky.feed.getAuthorFeed", params)
        if not data:
            break
        feed = data.get("feed") or []
        if not feed:
            break
        for item in feed:
            post = item.get("post") or {}
            is_repost = (item.get("reason") or {}).get("$type", "").endswith("reasonRepost")
            if is_repost and not include_reposts:
                continue
            parsed = _parse_post(post, handle)
            if since and (parsed.get("createdAt") or "") < since:
                # Feed is newest-first; once we're past the cutoff we can stop.
                return results[:max_posts]
            results.append(parsed)
            if len(results) >= max_posts:
                break
        cursor = data.get("cursor")
        if not cursor:
            break
    return results[:max_posts]
