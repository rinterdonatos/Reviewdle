"""
Builds a big TITLE -> YEAR map (no reviews) for Reviewdle's autocomplete/guess
box. The idea: the box a player types into should let them guess pretty much
any movie they can think of, not just the ~600 titles that can actually BE
the answer -- otherwise a curious player could view the page source, see the
datalist, and realize the answer must be one of a short list. Every option
in the dropdown also needs a "(year)" tag, so this version captures release
year alongside title.

This is much faster than build_review_db.py because it doesn't fetch reviews
or summaries -- just id + title + release date per page of results (20 movies
per API call), so scanning tens of thousands of titles takes minutes, not
hours.

Usage:
    python3 build_title_list.py YOUR_TMDB_API_KEY --out reviewdle_titles.json

Combines several TMDb /discover/movie sort strategies with a low vote-count
floor to maximize coverage (popular blockbusters AND obscure/indie titles),
dedupes by TMDb id, and writes out a JSON object of {"Title": "Year", ...}.
"""

import sys
import time
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error

BASE = "https://api.themoviedb.org/3"

# (sort_by, vote_count.gte) -- lower thresholds than build_review_db.py since
# we don't need review coverage, just the title to exist.
STRATEGIES = [
    ("popularity.desc", 1),
    ("vote_count.desc", 1),
    ("vote_average.desc", 20),
    ("revenue.desc", 1),
    ("primary_release_date.desc", 1),
    ("primary_release_date.asc", 1),
]


def api_get(path, api_key, retries=3, **params):
    params["api_key"] = api_key
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "reviewdle-titles/1.0"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                time.sleep(2 + attempt * 2)
                continue
            raise
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            raise


def collect_titles(api_key, strategies=STRATEGIES, max_pages=500):
    seen_ids = set()
    title_year = {}  # title -> year, first strategy to see a title wins (popularity.desc goes first)
    for sort_by, min_votes in strategies:
        page = 1
        got_this_strategy = 0
        while page <= max_pages:
            try:
                data = api_get(
                    "/discover/movie", api_key,
                    sort_by=sort_by,
                    **{"vote_count.gte": min_votes},
                    include_adult="false",
                    page=page,
                )
            except Exception as e:
                print(f"  [error] {sort_by} page {page}: {e}", file=sys.stderr)
                break
            results = data.get("results", [])
            if not results:
                break
            for m in results:
                mid = m["id"]
                if mid in seen_ids:
                    continue
                seen_ids.add(mid)
                t = (m.get("title") or "").strip()
                y = (m.get("release_date") or "")[:4]
                if t and t not in title_year:
                    title_year[t] = y  # may be "" if release date unknown
                    got_this_strategy += 1
            if page >= data.get("total_pages", 1):
                break
            page += 1
            if page % 50 == 0:
                print(f"  ...{sort_by} page {page}, total unique titles so far: {len(title_year)}")
            time.sleep(0.02)
        print(f"strategy '{sort_by}' (vote_count>={min_votes}) added {got_this_strategy} new titles; running total {len(title_year)}")
    return title_year


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("api_key")
    ap.add_argument("--out", default="reviewdle_titles.json")
    args = ap.parse_args()

    print("Collecting movie titles + years across multiple TMDb discovery strategies...")
    title_year = collect_titles(args.api_key)
    print(f"\nDone. {len(title_year)} unique titles collected.")

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(title_year, f, indent=2, ensure_ascii=False)
    print(f"Saved to {args.out}")


if __name__ == "__main__":
    main()
