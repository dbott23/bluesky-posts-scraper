# Bluesky Posts Scraper

Export Bluesky posts by **keyword search** or **user profile** — no browser required. Get post text, author, engagement metrics, timestamps, and embedded media URLs in a clean JSON or CSV dataset. Works with the public AT Protocol API.

## What it does

- **Keyword search** — search Bluesky for any term and collect matching posts (requires Bluesky credentials for search)
- **Profile scraping** — scrape posts from any public Bluesky profile without credentials
- Filter by date range, include or exclude replies and reposts
- Returns structured data ready to export as JSON, CSV, or Excel

## Use cases

- **Social listening** — track mentions of your brand, product, or topic on Bluesky
- **Trend research** — collect posts around a hashtag or keyword for analysis
- **Competitor monitoring** — see what's being posted about competitors
- **Influencer research** — pull posts from specific Bluesky accounts
- **Sentiment analysis** — feed posts into NLP pipelines or AI models
- **Dataset building** — create Bluesky post datasets for research or fine-tuning

## Input

| Field | Type | Description |
|---|---|---|
| `searchQueries` | string[] | Keywords to search (e.g. `["AI tools", "#buildinpublic"]`). Requires Bluesky credentials. |
| `profiles` | string[] | Bluesky handles to scrape (e.g. `["jack.bsky.social"]`). Public — no credentials needed. |
| `maxPosts` | integer | Max posts to collect per query or profile (default: `100`). |
| `sortBy` | string | `latest` (default) or `top`. |
| `sinceDate` | string | Only collect posts after this date (ISO format: `"2025-01-01"`). |
| `includeReplies` | boolean | Include reply posts when scraping profiles (default: `false`). |
| `includeReposts` | boolean | Include reposts when scraping profiles (default: `false`). |
| `blueskyIdentifier` | string | Your Bluesky handle or email (required for keyword search). |
| `blueskyAppPassword` | string | Your Bluesky app password (required for keyword search). Create one at Settings → App Passwords. |

At least one of `searchQueries` or `profiles` must be provided.

> **Note:** Keyword search requires a Bluesky account. Profile scraping is public and does not require credentials.

## Output

Each result is one post:

```json
{
  "uri": "at://did:plc:abc123/app.bsky.feed.post/xyz789",
  "cid": "bafyreig...",
  "author_handle": "alice.bsky.social",
  "author_display_name": "Alice",
  "text": "Just shipped a new feature! #buildinpublic",
  "created_at": "2026-07-20T14:32:00Z",
  "like_count": 42,
  "repost_count": 11,
  "reply_count": 5,
  "is_reply": false,
  "is_repost": false,
  "embed_type": null,
  "embed_url": null,
  "query": "#buildinpublic",
  "post_url": "https://bsky.app/profile/alice.bsky.social/post/xyz789"
}
```

## Pricing

This actor uses **Pay per result** pricing:

- **$1.00 per 1,000 posts** scraped
- A run collecting 200 posts costs **~$0.20**

## Frequently asked questions

**Do I need a Bluesky account to use this?**
For keyword/hashtag search: yes, you need a Bluesky handle and app password. For profile scraping (collecting posts from a specific user), no credentials are needed — public profiles are accessible via the AT Protocol API.

**How do I create an app password?**
Log in to Bluesky → Settings → Privacy & Security → App Passwords → Add App Password. Use the generated password as `blueskyAppPassword`. Do not use your main account password.

**What's the maximum number of posts I can collect?**
Set `maxPosts` up to any number. In practice, Bluesky's search API paginates in batches of 100. Very high limits on keyword searches may be rate-limited — 500–1,000 posts per query is a reliable range.

**Can I filter posts by date?**
Yes. Set `sinceDate` to an ISO date string (e.g. `"2026-01-01"`) to only collect posts after that date.

---

## More from dbott23

| Actor | What it does |
|---|---|
| [App Store & Google Play Reviews Scraper](https://apify.com/dbott23/appstore-reviews-scraper) | Export iOS and Android app reviews by keyword or app ID |
| [Trustpilot Reviews Scraper](https://apify.com/dbott23/trustpilot-reviews-scraper) | Export Trustpilot reviews to CSV or JSON — no API key needed |
| [B2B Reviews Scraper](https://apify.com/dbott23/b2b-reviews-scraper) | Pull reviews from G2, Capterra, and Trustpilot in one run |
| [AI Brand Visibility Tracker](https://apify.com/dbott23/ai-brand-visibility-tracker) | Track how AI assistants mention your brand vs. competitors |
| [AI Citation Auditor](https://apify.com/dbott23/ai-citation-auditor) | Check if your website is cited by ChatGPT, Perplexity, and Gemini |
