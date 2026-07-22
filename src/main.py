"""Bluesky Posts Scraper — scrapes posts by keyword search or profile."""

import asyncio

import httpx
from apify import Actor

from src.scrapers import bluesky


async def main() -> None:
    async with Actor:
        inp = await Actor.get_input() or {}

        queries: list[str] = inp.get("searchQueries") or []
        profiles: list[str] = inp.get("profiles") or []
        max_posts: int = int(inp.get("maxPosts") or 100)
        sort_by: str = inp.get("sortBy") or "latest"
        since: str | None = inp.get("sinceDate") or None
        include_replies: bool = bool(inp.get("includeReplies"))
        include_reposts: bool = bool(inp.get("includeReposts"))

        if not queries and not profiles:
            await Actor.fail(
                status_message="Input must include at least one search query or profile handle."
            )
            return

        total = 0
        async with httpx.AsyncClient() as client:
            for query in queries:
                Actor.log.info(f"Searching posts for: {query!r}")
                try:
                    posts = await bluesky.search_posts(
                        client, query, max_posts, sort=sort_by, since=since
                    )
                except Exception as exc:
                    Actor.log.warning(f"Search failed for {query!r}: {exc}")
                    continue
                if posts:
                    await Actor.push_data(posts)
                    total += len(posts)
                Actor.log.info(f"  → {len(posts)} posts for {query!r} (total: {total})")

            for profile in profiles:
                Actor.log.info(f"Scraping profile: {profile}")
                try:
                    posts = await bluesky.profile_posts(
                        client,
                        profile,
                        max_posts,
                        include_replies=include_replies,
                        include_reposts=include_reposts,
                        since=since,
                    )
                except Exception as exc:
                    Actor.log.warning(f"Profile scrape failed for {profile}: {exc}")
                    continue
                if posts:
                    await Actor.push_data(posts)
                    total += len(posts)
                Actor.log.info(f"  → {len(posts)} posts for {profile} (total: {total})")

        Actor.log.info(f"Done. Total posts pushed: {total}")


if __name__ == "__main__":
    asyncio.run(main())
