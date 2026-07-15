"""
Builds a Reviewdle-ready movie database using REAL reviews pulled from TMDb's
public API (themoviedb.org). Requires a free TMDb API key (v3 "API Key").

BASIC usage (first run):
    python3 build_review_db.py YOUR_TMDB_API_KEY --out reviewdle_data.json

TOP-UP usage (fetch only NEW movies not already in your existing dataset):
    python3 build_review_db.py YOUR_TMDB_API_KEY \
        --exclude-file reviewdle_data.json \
        --out reviewdle_data_more.json

What it does:
1. Discovers a large pool of candidate movies via /discover/movie, combining
   several sort strategies (popularity, vote count, vote average, revenue,
   release date) so the pool covers far more than just "currently trending"
   titles. Each strategy is capped at TMDb's page-500 limit, then everything
   is deduplicated by TMDb id.
2. Skips any movie whose title is already in --exclude-file, if provided.
3. For each remaining candidate, pulls its reviews via /movie/{id}/reviews.
4. Filters reviews down to real, substantial, English-language text (drops
   one-liners, non-English content, and duplicate/near-duplicate reviews).
5. Redacts the movie's own title (including "Director's Title" style prefixes
   and the title's distinctive core word) from review text, so a review
   doesn't hand you the answer outright.
6. Scores each review on a rough "spoiler-ness" scale (length, presence of
   spoiler-flag words like "ending"/"twist"/"dies", proper-noun density) and
   sorts a movie's reviews from vaguest -> most revealing.
7. Keeps only movies with >= 6 usable reviews after filtering, and writes
   them out as JSON: title, year, tmdb_id, six ordered review excerpts (each
   with author + a link back to TMDb for attribution), and a short plot
   summary sourced from TMDb's own synopsis field.
8. Saves progress incrementally (every 25 qualifying movies) so a long run
   can be safely interrupted and still leave you a usable partial file.

Realistic expectations: TMDb's review coverage is thin -- most movies have
zero or one review. Scanning "everything TMDb has" means walking through
tens of thousands of candidates, at roughly 2 API calls each, which can take
several hours. Progress prints as it goes so you can gauge pace and stop
early if needed (the partial --out file up to that point is still usable).
"""

import os
import sys
import re
import time
import json
import html
import argparse
import urllib.request
import urllib.parse
import urllib.error

BASE = "https://api.themoviedb.org/3"

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
MAX_WORDS = 120  # excerpt length cap; longer reviews get trimmed to first N sentences
REVIEWS_PER_MOVIE = 6

# (sort_by, vote_count.gte) pairs -- combined & deduped to build a much wider pool
DISCOVER_STRATEGIES = [
    ("popularity.desc", 50),
    ("vote_count.desc", 20),
    ("vote_average.desc", 100),
    ("revenue.desc", 10),
    ("primary_release_date.desc", 50),
]


def api_get(path, api_key, retries=3, **params):
    params["api_key"] = api_key
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "reviewdle-builder/1.0"})
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


def clean_text(raw):
    text = html.unescape(raw or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def first_n_sentences(text, max_words=MAX_WORDS):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = []
    count = 0
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
    base = re.sub(r"[:\-–].*$", "", t).strip()
    variants.add(base)
    if m:
        base2 = re.sub(r"[:\-–].*$", "", m.group(2)).strip()
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
    t = re.sub(r"[:\-–].*$", "", t).strip()
    t = re.sub(r'^(The|A|An)\s+', '', t, flags=re.IGNORECASE)
    words = re.findall(r"[A-Za-z']+", t)
    if not words:
        return None
    last = words[-1]
    if len(last) < 4 or last.lower() in COMMON_STOP:
        return None
    return last


def _pattern_for(phrase):
    esc = re.escape(phrase).replace(r"\'", "['’]")
    return re.compile(r"(?<![A-Za-z0-9])" + esc + r"(?![A-Za-z0-9])", re.IGNORECASE)


def _loose_pattern_for(phrase):
    words = phrase.split()
    if len(words) < 2:
        return None
    parts = [re.escape(w).replace(r"\'", "['’]") for w in words]
    joined = r"[^A-Za-z0-9]{0,3}".join(parts)
    return re.compile(r"(?<![A-Za-z0-9])" + joined + r"(?![A-Za-z])", re.IGNORECASE)


def redact_title(text, title):
    variants = sorted(build_title_variants(title), key=len, reverse=True)
    for v in variants:
        text = _pattern_for(v).sub("this film", text)
        loose = _loose_pattern_for(v)
        if loose:
            text = loose.sub("this film", text)
    cw = core_word(title)
    if cw:
        text = _pattern_for(cw).sub("this film", text)
    # collapse doubled placeholders like "this film's this film"
    text = re.sub(r"this film(?:['’]s)?\s+this film", "this film", text, flags=re.IGNORECASE)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def spoiler_score(text):
    lower = text.lower()
    score = 0.0
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
    return True


HARD_BLOCK = [
    re.compile(r"\bnigg", re.IGNORECASE),
    re.compile(r"\bfaggot\b", re.IGNORECASE),
    re.compile(r"\bcunt\b", re.IGNORECASE),
    re.compile(r"pizzagate", re.IGNORECASE),
    re.compile(r"\bretard\w*\b.{0,40}\b(hot|banging|baby)\b", re.IGNORECASE),
    re.compile(r"\b(hot|banging|baby)\b.{0,40}\bretard\w*\b", re.IGNORECASE),
]


def review_ok(text):
    return not any(p.search(text) for p in HARD_BLOCK)


def discover_pool(api_key, strategies=DISCOVER_STRATEGIES, max_pages=500):
    seen_ids = set()
    pool = []
    for sort_by, min_votes in strategies:
        page = 1
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
                print(f"  [discover error] {sort_by} page {page}: {e}", file=sys.stderr)
                break
            results = data.get("results", [])
            if not results:
                break
            for m in results:
                if m["id"] in seen_ids:
                    continue
                seen_ids.add(m["id"])
                pool.append((m["id"], m.get("title"), (m.get("release_date") or "")[:4]))
            if page >= data.get("total_pages", 1):
                break
            page += 1
            time.sleep(0.05)
        print(f"  strategy '{sort_by}' (vote_count>={min_votes}) done, pool size now {len(pool)}")
    return pool


def fetch_reviews(api_key, movie_id):
    reviews = []
    page = 1
    while True:
        data = api_get(f"/movie/{movie_id}/reviews", api_key, language="en-US", page=page)
        results = data.get("results", [])
        reviews.extend(results)
        if page >= data.get("total_pages", 1) or page >= 3:
            break
        page += 1
        time.sleep(0.05)
    return reviews


def fetch_overview(api_key, movie_id):
    data = api_get(f"/movie/{movie_id}", api_key, language="en-US")
    return clean_text(data.get("overview", ""))


def build_movie_entry(api_key, movie_id, title, year):
    raw_reviews = fetch_reviews(api_key, movie_id)
    if len(raw_reviews) < REVIEWS_PER_MOVIE:
        return None

    seen_snippets = set()
    candidates = []
    for r in raw_reviews:
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

    if len(candidates) < REVIEWS_PER_MOVIE:
        return None

    candidates.sort(key=lambda c: c["score"])
    chosen = candidates[:REVIEWS_PER_MOVIE]

    summary = fetch_overview(api_key, movie_id)
    if not summary:
        return None

    return {
        "title": title,
        "year": year,
        "tmdb_id": movie_id,
        "reviews": [{"text": c["text"], "author": c["author"], "url": c["url"]} for c in chosen],
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
    ap.add_argument("api_key")
    ap.add_argument("--target", type=int, default=100000, help="stop once this many NEW movies qualify (default: effectively unlimited)")
    ap.add_argument("--exclude-file", default=None, help="existing dataset JSON whose titles should be skipped (for topping up)")
    ap.add_argument("--out", default="reviewdle_data.json")
    ap.add_argument("--save-every", type=int, default=25, help="write partial progress every N qualifying movies")
    args = ap.parse_args()

    excluded = load_excluded_titles(args.exclude_file)
    if excluded:
        print(f"Excluding {len(excluded)} titles already in {args.exclude_file}")

    print("Discovering candidate pool across multiple TMDb sort strategies (this alone can take a few minutes)...")
    pool = discover_pool(args.api_key)
    print(f"Total deduplicated candidate pool: {len(pool)}")

    results = []
    scanned = 0
    skipped_existing = 0
    for movie_id, title, year in pool:
        if title and title.strip().lower() in excluded:
            skipped_existing += 1
            continue
        scanned += 1
        try:
            entry = build_movie_entry(args.api_key, movie_id, title, year)
        except Exception as e:
            entry = None
            print(f"  [skip] {title}: {e}", file=sys.stderr)
        if entry:
            results.append(entry)
            print(f"  [{len(results)}] {title} ({year}) -- qualified")
            if len(results) % args.save_every == 0:
                with open(args.out, "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
        if scanned % 200 == 0:
            print(f"...scanned {scanned} new candidates ({skipped_existing} already-owned skipped), qualifying so far: {len(results)}")
        if len(results) >= args.target:
            break
        time.sleep(0.02)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nDone. Scanned {scanned} new candidates ({skipped_existing} already-owned skipped),")
    print(f"{len(results)} qualified with >= {REVIEWS_PER_MOVIE} usable reviews.")
    print(f"Saved to {args.out}")


if __name__ == "__main__":
    main()
