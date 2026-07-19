"""
Second pass at building Reviewdle's answer pool -- this time combining TMDb
AND Trakt.tv reviews/comments for each candidate movie, so titles that fell
short of 6 usable TMDb reviews on their own can now clear the bar by pulling
in Trakt's separate user base too.

Requires:
  - A free TMDb API key (v3 "API Key") -- same one used for build_review_db.py
  - A free Trakt Client ID -- from https://app.trakt.tv/settings/apps/api
    (only the Client ID is needed; public comments don't require the OAuth
    login flow, just the trakt-api-key header)

Usage:
    python3 build_trakt_reviews.py TMDB_API_KEY TRAKT_CLIENT_ID \
        --exclude-file reviewdle_data_current.json \
        --out reviewdle_data_trakt.json

What it does:
1. Discovers a large candidate pool via TMDb /discover/movie (same multi
   -strategy approach as build_review_db.py), skipping any title already in
   --exclude-file.
2. For each candidate:
     a. Pulls TMDb reviews via /movie/{id}/reviews (as before).
     b. Looks up the same movie on Trakt via /search/tmdb/{id}?type=movie,
        then pulls its comments via /movies/{trakt_id}/comments/newest.
     c. Pools both sources together as candidate quotes.
3. Filters pooled candidates down to real, substantial, English-language
   text (drops one-liners, duplicates, non-English content).
4. Redacts the movie's own title (including "Director's Title" style
   prefixes and the title's distinctive core word) from every quote.
5. Scores each quote on a rough "spoiler-ness" scale (length, spoiler-flag
   words, proper-noun density, and Trakt's own spoiler flag when present)
   and sorts a movie's quotes from vaguest -> most revealing.
6. Keeps only movies with >= 6 usable quotes pooled from BOTH sources
   combined, and writes them out in the same JSON shape as
   build_review_db.py: title, reviews (each with text/author/url), summary.
7. Saves progress incrementally so a long run can be safely interrupted.

Realistic expectations: this still won't rescue every thin title -- some
movies just don't have much written about them anywhere. But combining two
independent review communities should meaningfully shrink the "not enough
material" pile compared to TMDb alone.
"""

import os
import sys
import re
import time
import json
import html
import argparse
import datetime
import urllib.request
import urllib.parse
import urllib.error

TMDB_BASE = "https://api.themoviedb.org/3"
TRAKT_BASE = "https://api.trakt.tv"

SPOILER_WORDS = [
    "ending", "ends with", "twist", "dies", "death of", "kills", "killed",
    "reveal", "reveals", "revealed", "spoiler", "in the end", "climax",
    "final scene", "he was dead", "she was dead", "all along"
]

COMMON_STOP = {
    'the', 'a', 'an', 'of', 'and', 'or', 'it', 'up', 'her', 'him', 'us', 'them',
    'this', 'that', 'is', 'in', 'on', 'part', 'chapter', 'story', 'one', 'out',
    'down', 'back', 'home', 'man', 'men', 'woman', 'women', 'love', 'life',
    'world', 'day', 'night', 'time', 'you', 'me', 'i', 'she', 'he', 'they',
    'we', 'my', 'your', 'his', 'their'
}

MIN_WORDS = 25
MAX_WORDS = 120
REVIEWS_PER_MOVIE = 6

DISCOVER_STRATEGIES = [
    ("popularity.desc", 50),
    ("vote_count.desc", 20),
    ("vote_average.desc", 100),
    ("revenue.desc", 10),
    ("primary_release_date.desc", 50),
]

HARD_BLOCK = [
    re.compile(r"\bnigg", re.IGNORECASE),
    re.compile(r"\bfaggot\b", re.IGNORECASE),
    re.compile(r"\bcunt\b", re.IGNORECASE),
    re.compile(r"pizzagate", re.IGNORECASE),
    re.compile(r"\bretard\w*\b.{0,40}\b(hot|banging|baby)\b", re.IGNORECASE),
    re.compile(r"\b(hot|banging|baby)\b.{0,40}\bretard\w*\b", re.IGNORECASE),
]


def api_get(url, headers, params=None, retries=3):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                time.sleep(2 + attempt * 2)
                continue
            if e.code == 404:
                return None
            raise
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            raise


def tmdb_get(path, api_key, **params):
    params = dict(params)
    params["api_key"] = api_key
    return api_get(f"{TMDB_BASE}{path}", headers={"User-Agent": "reviewdle/1.0"}, params=params)


def trakt_get(path, client_id, **params):
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": client_id,
        "User-Agent": "reviewdle/1.0",
    }
    return api_get(f"{TRAKT_BASE}{path}", headers=headers, params=params or None)


def clean_text(raw):
    text = html.unescape(raw or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def first_n_sentences(text, max_words=MAX_WORDS):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out, count = [], 0
    for s in sentences:
        w = len(s.split())
        if count + w > max_words and out:
            break
        out.append(s)
        count += w
        if count >= max_words:
            break
    return " ".join(out).strip()


def norm_quotes(s):
    return s.replace('’', "'").replace('‘', "'")


def build_title_variants(title):
    t = norm_quotes(title)
    variants = {t}
    m = re.match(r"^(.*?)'s\s+(.+)$", t)
    if m:
        prefix, suffix = m.group(1).strip(), m.group(2).strip()
        variants.add(suffix)
        if len(prefix) >= 3:
            variants.add(prefix)
    base = re.sub(r"(?:\s*:\s*|\s+[-–]\s+).*$", "", t).strip()
    variants.add(base)
    if m:
        base2 = re.sub(r"(?:\s*:\s*|\s+[-–]\s+).*$", "", m.group(2)).strip()
        variants.add(base2)
    more = set()
    for v in list(variants):
        v2 = re.sub(r'^(The|A|An)\s+', '', v, flags=re.IGNORECASE)
        if v2 != v:
            more.add(v2)
    variants |= more
    return {v.strip() for v in variants if len(v.strip()) >= 3}


def core_word(title):
    t = norm_quotes(title)
    m = re.match(r"^.*?'s\s+(.+)$", t)
    if m:
        t = m.group(1)
    t = re.sub(r"(?:\s*:\s*|\s+[-–]\s+).*$", "", t).strip()
    t = re.sub(r'^(The|A|An)\s+', '', t, flags=re.IGNORECASE)
    words = re.findall(r"[A-Za-z']+", t)
    if not words:
        return None
    last = words[-1]
    if len(last) < 4 or last.lower() in COMMON_STOP:
        return None
    return last


def pattern_for(phrase):
    esc = re.escape(phrase).replace(r"\'", "['’]")
    return re.compile(r"(?<![A-Za-z0-9])" + esc + r"(?![A-Za-z0-9])", re.IGNORECASE)


def loose_pattern_for(phrase):
    words = phrase.split()
    if len(words) < 2:
        return None
    parts = [re.escape(w).replace(r"\'", "['’]") for w in words]
    joined = r"[^A-Za-z0-9]{0,3}".join(parts)
    return re.compile(r"(?<![A-Za-z0-9])" + joined + r"(?![A-Za-z])", re.IGNORECASE)


def redact_title(text, title):
    variants = sorted(build_title_variants(title), key=len, reverse=True)
    for v in variants:
        text = pattern_for(v).sub("[this movie]", text)
        loose = loose_pattern_for(v)
        if loose:
            text = loose.sub("[this movie]", text)
    cw = core_word(title)
    if cw:
        text = pattern_for(cw).sub("[this movie]", text)
    text = re.sub(r"\[this movie\](?:['’]s)?\s+\[this movie\]", "[this movie]", text, flags=re.IGNORECASE)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def spoiler_score(text, extra=0):
    lower = text.lower()
    score = float(extra)
    score += len(text.split()) * 0.5
    for w in SPOILER_WORDS:
        if w in lower:
            score += 40
    cap_words = re.findall(r"(?<!^)(?<!\. )\b[A-Z][a-z]{2,}\b", text)
    score += len(cap_words) * 3
    return score


def is_usable(text):
    words = text.split()
    if len(words) < MIN_WORDS:
        return False
    letters = sum(c.isalpha() for c in text)
    if letters < len(text) * 0.6:
        return False
    # Reject text that's mostly non-Latin script (Arabic, Cyrillic, CJK, etc.)
    # -- TMDb reviews are filtered to en-US already, but Trakt comments are
    # global and unfiltered, so this catches non-English shouts that would
    # otherwise sneak past the word-count/letter-ratio checks above.
    non_latin = sum(1 for c in text if c.isalpha() and ord(c) > 0x2AF)
    if non_latin > letters * 0.15:
        return False
    return True


def review_ok(text):
    return not any(p.search(text) for p in HARD_BLOCK)


def discover_pool(api_key, strategies=DISCOVER_STRATEGIES, max_pages=500):
    seen_ids = set()
    pool = []
    for sort_by, min_votes in strategies:
        page = 1
        while page <= max_pages:
            try:
                data = tmdb_get(
                    "/discover/movie", api_key,
                    sort_by=sort_by,
                    **{"vote_count.gte": min_votes},
                    include_adult="false",
                    page=page,
                )
            except Exception as e:
                print(f"  [discover error] {sort_by} page {page}: {e}", file=sys.stderr)
                break
            results = (data or {}).get("results", [])
            if not results:
                break
            for m in results:
                if m["id"] in seen_ids:
                    continue
                seen_ids.add(m["id"])
                release_date = m.get("release_date") or ""
                pool.append((m["id"], m.get("title"), release_date[:4], release_date))
            if page >= (data or {}).get("total_pages", 1):
                break
            page += 1
            time.sleep(0.05)
        print(f"  strategy '{sort_by}' (vote_count>={min_votes}) done, pool size now {len(pool)}")
    return pool


def fetch_tmdb_reviews(api_key, movie_id):
    reviews = []
    page = 1
    while True:
        data = tmdb_get(f"/movie/{movie_id}/reviews", api_key, language="en-US", page=page)
        if not data:
            break
        results = data.get("results", [])
        reviews.extend(results)
        if page >= data.get("total_pages", 1) or page >= 3:
            break
        page += 1
        time.sleep(0.05)
    return reviews


def fetch_tmdb_overview(api_key, movie_id):
    data = tmdb_get(f"/movie/{movie_id}", api_key, language="en-US")
    return clean_text((data or {}).get("overview", ""))


def trakt_lookup(client_id, tmdb_id):
    data = trakt_get(f"/search/tmdb/{tmdb_id}", client_id, type="movie")
    if not data:
        return None
    for entry in data:
        movie = entry.get("movie")
        if movie:
            ids = movie.get("ids", {})
            return ids.get("trakt"), ids.get("slug")
    return None


def fetch_trakt_comments(client_id, trakt_id):
    comments = []
    page = 1
    while page <= 3:
        data = trakt_get(f"/movies/{trakt_id}/comments/newest", client_id, page=page, limit=50)
        if not data:
            break
        comments.extend(data)
        if len(data) < 50:
            break
        page += 1
        time.sleep(0.05)
    return comments


def build_movie_entry(tmdb_key, trakt_id_client, movie_id, title, year):
    candidates = []
    seen_snippets = set()

    # --- TMDb reviews ---
    for r in fetch_tmdb_reviews(tmdb_key, movie_id):
        text = clean_text(r.get("content", ""))
        text = first_n_sentences(text)
        if not is_usable(text):
            continue
        key = text[:60].lower()
        if key in seen_snippets:
            continue
        seen_snippets.add(key)
        redacted = redact_title(text, title)
        if not review_ok(redacted):
            continue
        candidates.append({
            "text": redacted,
            "author": r.get("author") or "Anonymous",
            "url": f"https://www.themoviedb.org/review/{r.get('id')}" if r.get("id") else None,
            "score": spoiler_score(redacted),
        })

    # --- Trakt comments ---
    trakt_client_id = trakt_id_client
    lookup = trakt_lookup(trakt_client_id, movie_id)
    if lookup:
        trakt_id, slug = lookup
        if trakt_id:
            for c in fetch_trakt_comments(trakt_client_id, trakt_id):
                text = clean_text(c.get("comment", ""))
                text = first_n_sentences(text)
                if not is_usable(text):
                    continue
                key = text[:60].lower()
                if key in seen_snippets:
                    continue
                seen_snippets.add(key)
                redacted = redact_title(text, title)
                if not review_ok(redacted):
                    continue
                bonus = 60 if c.get("spoiler") else 0
                username = (c.get("user") or {}).get("username") or "Anonymous"
                url = f"https://trakt.tv/movies/{slug}/comments/{c.get('id')}" if slug and c.get("id") else None
                candidates.append({
                    "text": redacted,
                    "author": username,
                    "url": url,
                    "score": spoiler_score(redacted, extra=bonus),
                    "source": "trakt",
                })

    if len(candidates) < REVIEWS_PER_MOVIE:
        return None

    candidates.sort(key=lambda c: c["score"])
    chosen = candidates[:REVIEWS_PER_MOVIE]

    summary = fetch_tmdb_overview(tmdb_key, movie_id)
    if not summary:
        return None

    return {
        "title": title,
        "year": year,
        "tmdb_id": movie_id,
        "reviews": [
            {
                "text": c["text"], "author": c["author"], "url": c["url"],
                "source": c.get("source", "tmdb"),
            }
            for c in chosen
        ],
        "summary": summary,
    }


def load_excluded_titles(path):
    if not path or not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {d["title"].strip().lower() for d in data if d.get("title")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tmdb_api_key")
    ap.add_argument("trakt_client_id")
    ap.add_argument("--target", type=int, default=100000, help="stop once this many NEW movies qualify")
    ap.add_argument("--exclude-file", default=None, help="existing dataset JSON whose titles should be skipped")
    ap.add_argument("--out", default="reviewdle_data_trakt.json")
    ap.add_argument("--save-every", type=int, default=25)
    args = ap.parse_args()

    excluded = load_excluded_titles(args.exclude_file)
    if excluded:
        print(f"Excluding {len(excluded)} titles already in {args.exclude_file}")

    print("Discovering candidate pool across multiple TMDb sort strategies...")
    pool = discover_pool(args.tmdb_api_key)
    print(f"Total deduplicated candidate pool: {len(pool)}")

    today = datetime.date.today().isoformat()
    results = []
    scanned = 0
    skipped_existing = 0
    skipped_unreleased = 0
    for movie_id, title, year, release_date in pool:
        if title and title.strip().lower() in excluded:
            skipped_existing += 1
            continue
        if not release_date or release_date > today:
            skipped_unreleased += 1
            continue
        scanned += 1
        try:
            entry = build_movie_entry(args.tmdb_api_key, args.trakt_client_id, movie_id, title, year)
        except Exception as e:
            entry = None
            print(f"  [skip] {title}: {e}", file=sys.stderr)
        if entry:
            results.append(entry)
            print(f"  [{len(results)}] {title} ({year}) -- qualified")
            if len(results) % args.save_every == 0:
                with open(args.out, "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
        if scanned % 100 == 0:
            print(f"...scanned {scanned} new candidates ({skipped_existing} already-owned, {skipped_unreleased} unreleased skipped), qualifying so far: {len(results)}")
        if len(results) >= args.target:
            break
        time.sleep(0.02)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nDone. Scanned {scanned} new candidates ({skipped_existing} already-owned, {skipped_unreleased} unreleased skipped),")
    print(f"{len(results)} qualified with >= {REVIEWS_PER_MOVIE} usable TMDb+Trakt quotes combined.")
    print(f"Saved to {args.out}")


if __name__ == "__main__":
    main()
