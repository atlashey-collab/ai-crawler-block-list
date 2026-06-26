#!/usr/bin/env python3
"""
check_robots.py - Check any site's robots.txt against the 10 AI crawlers that matter.

Part of the "AI Crawler Block List 2026" open dataset by AI Tools Insider.
  https://aitoolsinsiderhq.com/ai-crawler-study.html

No dependencies (Python 3 standard library only).

Usage:
    python3 check_robots.py https://example.com      # fetch a live site's robots.txt
    python3 check_robots.py example.com              # scheme optional
    cat robots.txt | python3 check_robots.py         # or pipe a robots.txt you already have

It uses the same precedence real crawlers use:
  - the most specific (longest-matching) User-agent group wins;
  - within the winning group, the longest matching path rule wins;
  - on an equal-length tie, Allow beats Disallow.
"""
import sys
import urllib.request
from urllib.parse import urlparse

# token -> (operator, group). "citation" bots decide whether an AI assistant
# can quote your page; blocking those is what costs you AI-search visibility.
BOTS = [
    ("GPTBot",          "OpenAI",        "training"),
    ("OAI-SearchBot",   "OpenAI",        "citation"),
    ("ChatGPT-User",    "OpenAI",        "citation"),
    ("ClaudeBot",       "Anthropic",     "training"),
    ("Claude-User",     "Anthropic",     "citation"),
    ("PerplexityBot",   "Perplexity",    "citation"),
    ("Perplexity-User", "Perplexity",    "citation"),
    ("Google-Extended", "Google",        "training"),
    ("CCBot",           "Common Crawl",  "training"),
    ("Bytespider",      "ByteDance",     "training"),
]

UA = "Mozilla/5.0 (compatible; AICrawlerBlockList/1.0; +https://aitoolsinsiderhq.com)"


def fetch_robots(target):
    """Return robots.txt text for a host (or '' if none)."""
    if "://" not in target:
        target = "https://" + target
    parsed = urlparse(target)
    url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        print(f"Could not fetch {url}: {e}", file=sys.stderr)
        return ""


def parse_groups(text):
    """Parse robots.txt into {lowercased user-agent: [(field, value), ...]}."""
    groups = {}
    current = []
    expecting_agent = True
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, _, value = line.partition(":")
        field = field.strip().lower()
        value = value.strip()
        if field == "user-agent":
            if not expecting_agent:
                current = []
            agent = value.lower()
            groups.setdefault(agent, [])
            current = groups[agent]
            expecting_agent = True
        elif field in ("allow", "disallow"):
            expecting_agent = False
            current.append((field, value))
    return groups


def rules_for(groups, token):
    """Most-specific matching group for a bot token (its own block, else '*')."""
    t = token.lower()
    if t in groups:
        return groups[t]
    return groups.get("*", [])


def is_blocked(rules, path="/"):
    """Apply longest-match precedence; Allow wins ties. True = blocked."""
    best_len = -1
    best_allowed = True  # default allow
    for field, value in rules:
        if value == "":
            # 'Disallow:' (empty) = allow everything; 'Allow:' empty = no-op
            if field == "disallow":
                if 0 > best_len:
                    best_len, best_allowed = 0, True
            continue
        if path.startswith(value):
            n = len(value)
            if n > best_len:
                best_len, best_allowed = n, (field == "allow")
            elif n == best_len and field == "allow":
                best_allowed = True
    return not best_allowed


def main():
    if not sys.stdin.isatty() and len(sys.argv) < 2:
        text = sys.stdin.read()
        label = "(piped robots.txt)"
    elif len(sys.argv) >= 2:
        text = fetch_robots(sys.argv[1])
        label = sys.argv[1]
    else:
        print(__doc__)
        sys.exit(1)

    groups = parse_groups(text)
    print(f"AI crawler access for {label}")
    blocked_total = blocked_citation = 0
    for token, operator, group in BOTS:
        blocked = is_blocked(rules_for(groups, token))
        state = "BLOCKED" if blocked else "ALLOWED"
        note = ""
        if blocked:
            blocked_total += 1
            if group == "citation":
                blocked_citation += 1
                note = "   <- invisible to this AI search engine"
        dots = "." * (16 - len(token))
        print(f"  {token}{dots} {state}  ({group}, {operator}){note}")
    print(
        f"Summary: {blocked_total} blocked, {len(BOTS) - blocked_total} allowed"
        f"  |  citation bots blocked: {blocked_citation}"
    )
    if blocked_citation:
        print("Tip: blocking *citation* bots costs you AI-search traffic. "
              "Block training bots if you must; keep citation bots open.")


if __name__ == "__main__":
    main()
