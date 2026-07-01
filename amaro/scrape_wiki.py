# amaro_wiki_dump.py
"""
Discover and download the entire Amaro Lab Wiki.

Subcommands:
    map      Enumerate every page, build a link-structure index → wiki_map.json
    scrape   Download every page as clean Markdown → amaro_wiki/

Requirements:
    pip install requests html2text

Usage:
    export WIKI_USER="your_username"
    export WIKI_PASS="your_password"

    python amaro_wiki_dump.py map
    python amaro_wiki_dump.py scrape
    python amaro_wiki_dump.py scrape --raw   # save raw wikitext instead
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

import requests

try:
    import html2text

    HAS_HTML2TEXT = True
except ImportError:
    HAS_HTML2TEXT = False


# ── Configuration ──────────────────────────────────────────────────────────────

API_URL = "https://wiki.amaro.ucsd.edu/mediawiki/api.php"

WIKI_USER = "zalibhai"
WIKI_PASS = "Spiderman7865110!"

DEFAULT_MAP_PATH = "wiki_map.json"
DEFAULT_OUTPUT_DIR = "amaro_wiki"
REQUEST_DELAY = 0.4


# ── Wiki API Client ───────────────────────────────────────────────────────────


class WikiClient:
    """Authenticated MediaWiki API client with pagination and rate limiting."""

    def __init__(self, api_url, username, password):
        self.api_url = api_url
        self.session = requests.Session()
        self._login(username, password)

    def _login(self, username, password):
        resp = self.session.get(
            self.api_url,
            params={
                "action": "query",
                "meta": "tokens",
                "type": "login",
                "format": "json",
            },
        )
        resp.raise_for_status()
        login_token = resp.json()["query"]["tokens"]["logintoken"]

        resp = self.session.post(
            self.api_url,
            data={
                "action": "login",
                "lgname": username,
                "lgpassword": password,
                "lgtoken": login_token,
                "format": "json",
            },
        )
        resp.raise_for_status()
        result = resp.json().get("login", {}).get("result")
        if result != "Success":
            raise RuntimeError(f"Wiki login failed: {result}")
        print(f"✓ Logged in as {username}")

    def _get(self, **params):
        """Single API GET request with automatic rate limiting."""
        params.setdefault("format", "json")
        time.sleep(REQUEST_DELAY)
        resp = self.session.get(self.api_url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_namespaces(self):
        """Return {ns_id: display_name} for all namespaces."""
        data = self._get(action="query", meta="siteinfo", siprop="namespaces")
        result = {}
        for ns_id, ns_info in data["query"]["namespaces"].items():
            name = ns_info.get("canonical") or ns_info.get("*") or f"ns{ns_id}"
            result[int(ns_id)] = name if name else "(Main)"
        return result

    def get_all_pages(self, namespace=0):
        """List every page in a namespace, handling pagination."""
        pages = []
        params = {
            "action": "query",
            "list": "allpages",
            "aplimit": "max",
            "apnamespace": namespace,
        }
        while True:
            data = self._get(**params)
            pages.extend(data["query"]["allpages"])
            if "continue" not in data:
                break
            params["apcontinue"] = data["continue"]["apcontinue"]
        return pages

    def get_page_metadata(self, title):
        """Fetch links, categories, revision info for a single page."""
        data = self._get(
            action="query",
            titles=title,
            prop="links|categories|revisions",
            pllimit="max",
            cllimit="max",
            rvprop="timestamp|size",
        )
        page = next(iter(data["query"]["pages"].values()))

        # Paginate links if the page has many outgoing links
        links = [link["title"] for link in page.get("links", [])]
        while "continue" in data and "plcontinue" in data.get("continue", {}):
            data = self._get(
                action="query",
                titles=title,
                prop="links",
                pllimit="max",
                plcontinue=data["continue"]["plcontinue"],
            )
            p = next(iter(data["query"]["pages"].values()))
            links.extend(link["title"] for link in p.get("links", []))

        categories = [cat["title"] for cat in page.get("categories", [])]
        rev = (page.get("revisions") or [{}])[0]

        return {
            "pageid": page.get("pageid"),
            "namespace": page.get("ns", 0),
            "links_to": sorted(set(links)),
            "categories": categories,
            "size_bytes": rev.get("size", 0),
            "last_modified": rev.get("timestamp", ""),
            "is_redirect": "redirect" in page,
        }

    def get_parsed_html(self, title):
        """Get server-rendered HTML via action=parse (follows redirects)."""
        data = self._get(
            action="parse",
            page=title,
            prop="text|displaytitle",
            disabletoc="1",
            redirects="1",
        )
        if "error" in data:
            raise RuntimeError(data["error"].get("info", "Parse error"))
        parse = data.get("parse", {})
        return {
            "title": parse.get("displaytitle", title),
            "html": parse.get("text", {}).get("*", ""),
        }

    def get_raw_wikitext(self, title):
        """Get raw wikitext for a page. Returns None if page doesn't exist."""
        data = self._get(
            action="query", titles=title, prop="revisions", rvprop="content"
        )
        page = next(iter(data["query"]["pages"].values()))
        if page.get("missing") is not None:
            return None
        revisions = page.get("revisions", [])
        return revisions[0]["*"] if revisions else None


# ── Conversion Helpers ─────────────────────────────────────────────────────────


def clean_mediawiki_html(html):
    """Strip MediaWiki UI elements before markdown conversion."""
    # Remove [edit] links on section headings
    html = re.sub(
        r'<span class="mw-editsection">.*?</span>', "", html, flags=re.DOTALL
    )
    # Remove table of contents block
    html = re.sub(r'<div id="toc".*?</div>\s*</div>', "", html, flags=re.DOTALL)
    return html


def html_to_markdown(html_content):
    """Convert MediaWiki HTML to clean Markdown."""
    cleaned = clean_mediawiki_html(html_content)

    if not HAS_HTML2TEXT:
        text = re.sub(r"<[^>]+>", "", cleaned)
        return re.sub(r"\n{3,}", "\n\n", text).strip()

    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.protect_links = True
    converter.wrap_links = False
    converter.unicode_snob = True
    converter.inline_links = True
    return converter.handle(cleaned).strip()


def sanitize_filename(title):
    """Wiki title → filesystem-safe filename (no extension added)."""
    name = title.strip().replace(" ", "_")
    name = re.sub(r"[^\w.\-~]", "_", name)
    return re.sub(r"_+", "_", name).strip("_")


# ── Map Subcommand ─────────────────────────────────────────────────────────────


def cmd_map(args):
    """Enumerate every page and write a structure map to JSON."""
    client = WikiClient(API_URL, WIKI_USER, WIKI_PASS)
    namespaces = [int(n) for n in args.namespaces.split(",")]
    ns_labels = client.get_namespaces()

    print(f"Scanning namespaces: {[ns_labels.get(n, n) for n in namespaces]}\n")

    all_pages = []
    for ns in namespaces:
        pages = client.get_all_pages(namespace=ns)
        print(f"  {ns_labels.get(ns, ns)}: {len(pages)} pages")
        all_pages.extend(pages)

    print(f"\nTotal: {len(all_pages)} pages — fetching metadata…\n")

    wiki_map = {
        "wiki_url": API_URL.replace("/api.php", ""),
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "namespaces_scanned": {str(n): ns_labels.get(n, "") for n in namespaces},
        "total_pages": len(all_pages),
        "pages": {},
    }

    for i, page in enumerate(all_pages, 1):
        title = page["title"]
        print(f"  [{i}/{len(all_pages)}] {title}")
        try:
            wiki_map["pages"][title] = client.get_page_metadata(title)
        except Exception as exc:
            print(f"    ⚠ {exc}")
            wiki_map["pages"][title] = {"error": str(exc)}

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(wiki_map, f, indent=2, ensure_ascii=False)

    # Summary stats
    existing_titles = set(wiki_map["pages"])
    all_linked = set()
    redirects = 0
    for pdata in wiki_map["pages"].values():
        all_linked.update(pdata.get("links_to", []))
        if pdata.get("is_redirect"):
            redirects += 1

    red_links = all_linked - existing_titles
    print(f"\n✓ Saved → {args.out}")
    print(f"  {len(wiki_map['pages'])} pages indexed")
    print(f"  {redirects} redirects")
    print(f"  {len(red_links)} red links (referenced but nonexistent)")


# ── Scrape Subcommand ──────────────────────────────────────────────────────────


def cmd_scrape(args):
    """Download every page as Markdown (or raw wikitext) files."""
    if not args.raw and not HAS_HTML2TEXT:
        print("⚠ html2text not installed — falling back to basic tag stripping.")
        print("  For cleaner output: pip install html2text\n")

    client = WikiClient(API_URL, WIKI_USER, WIKI_PASS)

    # Load page list from map file or enumerate fresh
    if args.map and os.path.exists(args.map):
        print(f"Loading page list from {args.map}")
        with open(args.map, encoding="utf-8") as f:
            wiki_map = json.load(f)
        titles = [
            t
            for t, meta in wiki_map["pages"].items()
            if not meta.get("is_redirect") and "error" not in meta
        ]
        print(f"  {len(titles)} pages (skipping redirects & errors)\n")
    else:
        print("No map file — enumerating pages from API…")
        namespaces = [int(n) for n in args.namespaces.split(",")]
        titles = []
        for ns in namespaces:
            titles.extend(p["title"] for p in client.get_all_pages(namespace=ns))
        print(f"  {len(titles)} pages found\n")

    os.makedirs(args.out, exist_ok=True)
    ext = ".txt" if args.raw else ".md"
    saved, skipped = 0, 0
    index_entries = []

    for i, title in enumerate(titles, 1):
        filename = sanitize_filename(title) + ext
        print(f"  [{i}/{len(titles)}] {title}")

        try:
            if args.raw:
                content = client.get_raw_wikitext(title)
                if content is None:
                    print("    ⚠ Page not found")
                    skipped += 1
                    continue
            else:
                result = client.get_parsed_html(title)
                if not result["html"].strip():
                    print("    ⚠ Empty page")
                    skipped += 1
                    continue
                md_body = html_to_markdown(result["html"])
                content = f"# {title}\n\n{md_body}"

            filepath = os.path.join(args.out, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
                f.write("\n")

            print(f"    ✓ {len(content):,} chars")
            index_entries.append({"title": title, "file": filename})
            saved += 1

        except Exception as exc:
            print(f"    ⚠ {exc}")
            skipped += 1

    _write_indices(args.out, index_entries)
    print(f"\n✓ Done! {saved} saved, {skipped} skipped → ./{args.out}/")


def _write_indices(output_dir, entries):
    """Generate _index.json and _index.md in the output directory."""
    sorted_entries = sorted(entries, key=lambda e: e["title"].lower())

    json_path = os.path.join(output_dir, "_index.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(entries), "pages": sorted_entries}, f, indent=2)

    md_path = os.path.join(output_dir, "_index.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Amaro Lab Wiki — Index\n\n")
        for entry in sorted_entries:
            f.write(f"- [{entry['title']}]({entry['file']})\n")
        f.write(f"\n---\n{len(entries)} pages total\n")


# ── CLI ────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Discover and download the Amaro Lab Wiki"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    map_p = sub.add_parser("map", help="Build a JSON structure map of the wiki")
    map_p.add_argument(
        "--out", default=DEFAULT_MAP_PATH, help="Output path (default: wiki_map.json)"
    )
    map_p.add_argument(
        "--namespaces", default="0", help="Comma-separated namespace IDs (default: 0)"
    )

    scrape_p = sub.add_parser("scrape", help="Download all pages as Markdown")
    scrape_p.add_argument(
        "--out", default=DEFAULT_OUTPUT_DIR, help="Output dir (default: amaro_wiki/)"
    )
    scrape_p.add_argument(
        "--map", default=DEFAULT_MAP_PATH, help="wiki_map.json to read page list from"
    )
    scrape_p.add_argument(
        "--raw", action="store_true", help="Save raw wikitext instead of Markdown"
    )
    scrape_p.add_argument(
        "--namespaces", default="0", help="Namespace IDs if no map file (default: 0)"
    )

    args = parser.parse_args()
    if args.command == "map":
        cmd_map(args)
    elif args.command == "scrape":
        cmd_scrape(args)


if __name__ == "__main__":
    main()
