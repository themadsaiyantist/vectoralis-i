"""Open every external link of the repository's Markdown pages, and print the ones that do not answer 200.

Run it from the repository root: `python3 tools/check_links.py` for every page, or name files and folders.
It needs the network, so it is not part of `tools/check.sh`. Run it before a page is called checked.
Reddit is skipped: it refuses automated requests. A page behind a bot challenge, such as Cloudflare's
"Just a moment", is alive for a person and says so to no checker: it is listed apart. Open both by hand.
Exit code 1 when a link does not answer 200.
"""
import concurrent.futures
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request

LINK = re.compile(r"\]\((https?://[^)\s]+)\)")
# A plain client name first. Some sites refuse a client that calls itself a browser, others refuse one that does not.
HEADERS = (
    {"User-Agent": "check_links/1.0", "Accept": "*/*"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0", "Accept": "text/html,*/*"},
)
RETRY_WITH_GET = (400, 403, 404, 405, 429, 501)


def _challenge(error):
    """Whether a refusal is a bot challenge page, which a person passes in a browser."""
    if error.headers.get("cf-mitigated") == "challenge":
        return True
    try:
        return b"Just a moment" in error.read(4096)
    except Exception:
        return False


def fetch(url):
    """The status a link answers: HEAD first, then GET for the servers that refuse HEAD, under each client name."""
    last = None
    for headers in HEADERS:
        for method in ("HEAD", "GET"):
            try:
                request = urllib.request.Request(url.split("#")[0], headers=headers, method=method)
                with urllib.request.urlopen(request, timeout=25) as answer:
                    return answer.status
            except urllib.error.HTTPError as error:
                last = error.code
                if method == "GET" and error.code in (403, 503) and _challenge(error):
                    return "challenge"
                if error.code not in RETRY_WITH_GET:
                    return error.code
            except Exception as error:
                last = type(error).__name__
    return last


def pages(names):
    """The Markdown files named, or every tracked one when none is named."""
    if not names:
        tracked = subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True, check=True).stdout
        return [pathlib.Path(p) for p in tracked.split()]
    out = []
    for name in names:
        path = pathlib.Path(name)
        out += [path] if path.is_file() else sorted(path.rglob("*.md"))
    return out


def main(argv):
    where = {}
    for path in pages(argv):
        for url in LINK.findall(path.read_text(encoding="utf-8")):
            where.setdefault(url, set()).add(str(path))
    urls = [u for u in where if "reddit.com" not in u]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        results = dict(zip(urls, pool.map(fetch, urls)))
    by_hand = sorted(u for u, s in results.items() if s == "challenge")
    bad = {u: s for u, s in results.items() if s not in (200, "challenge")}
    print(f"{len(urls)} links opened, {len(bad)} did not answer 200, {len(where) - len(urls)} reddit links skipped")
    for url in by_hand:
        print(f"  behind a bot challenge, open by hand: {url}  ({', '.join(sorted(where[url]))})")
    for url, status in sorted(bad.items(), key=lambda kv: str(kv[1])):
        print(f"  {status}  {url}  ({', '.join(sorted(where[url]))})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
