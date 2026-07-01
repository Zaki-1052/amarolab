# scrape_amaro_scripts.py
"""
Scrape all scripts from the Amaro Lab Wiki ScriptsMain page.

Requirements:
    pip install requests

Usage:
    python scrape_amaro_scripts.py
    python scrape_amaro_scripts.py --dry-run
"""

import os
import re
import sys
import time
import requests

API_URL = "https://wiki.amaro.ucsd.edu/mediawiki/api.php"
OUTPUT_DIR = "amaro_scripts"

# Replace these with your actual wiki credentials
WIKI_USER = "zalibhai"
WIKI_PASS = "Spiderman7865110!"


def create_session():
    """Log in to the wiki and return an authenticated session."""
    session = requests.Session()

    token_resp = session.get(API_URL, params={
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json",
    })
    token_resp.raise_for_status()
    login_token = token_resp.json()["query"]["tokens"]["logintoken"]

    login_resp = session.post(API_URL, data={
        "action": "login",
        "lgname": WIKI_USER,
        "lgpassword": WIKI_PASS,
        "lgtoken": login_token,
        "format": "json",
    })
    login_resp.raise_for_status()
    result = login_resp.json().get("login", {}).get("result")
    if result != "Success":
        raise RuntimeError(f"Wiki login failed: {result}")

    print(f"Logged in as {WIKI_USER}")
    return session


def get_script_titles(session):
    """
    Fetch ScriptsMain raw wikitext and extract all [[filename.ext]] links.
    MediaWiki normalizes these titles (first letter capitalized,
    underscores become spaces), so passing them directly to the
    revisions API works.
    """
    resp = session.get(API_URL, params={
        "action": "query",
        "titles": "ScriptsMain",
        "prop": "revisions",
        "rvprop": "content",
        "format": "json",
    })
    resp.raise_for_status()

    pages = resp.json()["query"]["pages"]
    wikitext = ""
    for page_data in pages.values():
        revisions = page_data.get("revisions", [])
        if revisions:
            wikitext = revisions[0]["*"]

    if not wikitext:
        raise RuntimeError("Could not fetch ScriptsMain wikitext")

    # Match [[title.ext]] or [[title.ext|display text]]
    raw_titles = re.findall(r'\[\[([^\]|]+\.\w+?)(?:\|[^\]]+)?\]\]', wikitext)

    # Deduplicate while preserving order
    seen = set()
    titles = []
    for t in raw_titles:
        normalized = t.strip()
        if normalized not in seen:
            seen.add(normalized)
            titles.append(normalized)

    print(f"Found {len(titles)} script pages on ScriptsMain")
    return titles


def fetch_page_wikitext(session, title):
    """Fetch raw wikitext of a single page. Returns None if page doesn't exist."""
    resp = session.get(API_URL, params={
        "action": "query",
        "titles": title,
        "prop": "revisions",
        "rvprop": "content",
        "format": "json",
    })
    resp.raise_for_status()

    pages = resp.json()["query"]["pages"]
    for page_id, page_data in pages.items():
        if page_id == "-1":
            return None
        revisions = page_data.get("revisions", [])
        if revisions:
            return revisions[0]["*"]
    return None


def strip_wiki_tags(wikitext):
    """
    Remove the <code><pre><nowiki>...</nowiki></pre></code> wrappers
    observed in the actual API responses. Also handles <source> and
    <syntaxhighlight> in case any pages use those instead.

    The raw wikitext from the API is already clean (no HTML entities),
    so no decoding step is needed.
    """
    text = wikitext
    for tag in ("code", "pre", "nowiki", "source", "syntaxhighlight"):
        text = re.sub(rf"<{tag}[^>]*>", "", text, flags=re.IGNORECASE)
        text = re.sub(rf"</{tag}\s*>", "", text, flags=re.IGNORECASE)
    return text.strip()


def title_to_filename(title):
    """
    Convert a wiki link target to a safe filename.
    'heat equation.py' -> 'heat_equation.py'
    '~math_sandbox.py' -> '~math_sandbox.py'
    """
    name = title.strip().replace(" ", "_")
    name = re.sub(r"[^\w.\-~]", "_", name)
    return name


def main():
    dry_run = "--dry-run" in sys.argv

    session = create_session()
    titles = get_script_titles(session)

    if dry_run:
        print("\n--- DRY RUN: listing titles only ---")
        for i, title in enumerate(titles, 1):
            print(f"  [{i:3d}] {title} -> {title_to_filename(title)}")
        print(f"\nTotal: {len(titles)} scripts")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    saved = 0
    skipped = 0

    for i, title in enumerate(titles, 1):
        filename = title_to_filename(title)
        print(f"[{i}/{len(titles)}] {title} -> {filename}")

        wikitext = fetch_page_wikitext(session, title)
        if wikitext is None:
            print("  ⚠ Page not found")
            skipped += 1
            continue

        code = strip_wiki_tags(wikitext)
        if not code:
            print("  ⚠ Empty after stripping tags")
            skipped += 1
            continue

        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
            f.write("\n")

        print(f"  ✓ Saved ({len(code)} chars)")
        saved += 1
        time.sleep(0.5)

    print(f"\nDone! {saved} saved, {skipped} skipped -> ./{OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
