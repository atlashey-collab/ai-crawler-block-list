# AI Crawler Block List 2026

**An open dataset of which AI crawlers the top AI & SaaS tools actually block in their `robots.txt` — plus a tiny script to check any site yourself.**

In June 2026 we fetched the **live `robots.txt` of 41 well-known AI and SaaS tools** (OpenAI, Anthropic, Google Gemini, Notion, Canva, Figma, HubSpot, Semrush, and more) and parsed each one against the **10 AI crawlers that matter most** — the bots that train models *and* the bots that fetch pages to cite them in answers.

The result is counterintuitive enough that we open-sourced the raw data so anyone can verify, reuse, or extend it.

## TL;DR — the finding

> **36 of 41 tools (88%) block *no* AI crawler at all.** Only 5 block anything. And of the handful that do block, most block the **wrong** bots.

The popular narrative is "AI companies are locking their content down." The data says the opposite: almost nobody is blocking, and the few who do mostly block *training* crawlers while leaving the *citation* crawlers (the ones that decide whether ChatGPT / Perplexity can quote you) untouched — or, in one case, block the citation crawlers and make themselves invisible in AI search.

### Key numbers

| Metric | Value |
| --- | --- |
| Tools studied | **41** |
| Block **nothing** | **36 (88%)** |
| Block **at least one** AI crawler | **5 (12%)** |
| Block **any citation** crawler (OAI-SearchBot / PerplexityBot / ChatGPT-User…) | **1 (2%)** |
| Block **any training** crawler (GPTBot / CCBot / Google-Extended…) | **5 (12%)** |
| Most-blocked single bot | **GPTBot** and **CCBot**, tied at **7%** |

### Who actually blocks something

| Tool | Domain | Bots blocked |
| --- | --- | --- |
| **Figma** | figma.com | GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, Google-Extended, CCBot |
| **Canva** | canva.com | GPTBot, ClaudeBot, CCBot, Bytespider |
| **Descript** | descript.com | Bytespider |
| **Loom** | loom.com | GPTBot |
| **Calendly** | calendly.com | CCBot |

**Two ways to read this table:**

- **Canva does it right (textbook).** It blocks only *training* crawlers (GPTBot, ClaudeBot, CCBot, Bytespider) and leaves every *citation* crawler open — so it protects its content from model training while staying fully quotable in ChatGPT and Perplexity.
- **Figma blocks the citation crawlers too** (OAI-SearchBot, PerplexityBot, ChatGPT-User). That makes Figma effectively **invisible in AI search** — when someone asks an AI assistant about design tools, Figma's own pages can't be fetched and cited.

> **The lesson for your own site:** blocking *training* bots is roughly free. Blocking *citation* bots quietly costs you AI-search traffic. Most teams that "lock down AI" never make that distinction — and accidentally block the bots they most want to keep.

## The 10 crawlers we checked

| Token | Operator | Type | What it does |
| --- | --- | --- | --- |
| `GPTBot` | OpenAI | training | Collects pages to train OpenAI models |
| `OAI-SearchBot` | OpenAI | **citation** | Fetches pages so ChatGPT can cite them |
| `ChatGPT-User` | OpenAI | **citation** | Live fetch when a user asks ChatGPT about a page |
| `ClaudeBot` | Anthropic | training | Collects pages to train Claude |
| `Claude-User` | Anthropic | **citation** | Live fetch for Claude answers |
| `PerplexityBot` | Perplexity | **citation** | Indexes pages for Perplexity answers |
| `Perplexity-User` | Perplexity | **citation** | Live fetch for Perplexity answers |
| `Google-Extended` | Google | training | Opts content in/out of Gemini training |
| `CCBot` | Common Crawl | training | Open web crawl used by many model trainers |
| `Bytespider` | ByteDance | training | ByteDance / TikTok crawler |

*"Citation" = bots that decide whether an AI assistant can quote your page in an answer. Blocking these is what costs you AI-search visibility.*

## What's in this repo

```
data/ai-crawler-blocklist.csv    # one row per tool, one column per bot (1 = blocked)
data/ai-crawler-blocklist.json   # same data + precomputed stats
check_robots.py                  # check ANY robots.txt against the 10 AI crawlers
LICENSE                          # MIT (code) — data is CC BY 4.0 (see "License" below)
```

## Check your own site

`check_robots.py` has **no dependencies** (Python 3 standard library only). It uses the same longest-match rule real crawlers use (a more specific `User-agent` block wins, and `Allow` overrides `Disallow` on an equal-length match).

```bash
# Check a live site
python3 check_robots.py https://example.com

# Or pipe a robots.txt you already have
cat robots.txt | python3 check_robots.py
```

Example output:

```
AI crawler access for example.com
  GPTBot............ ALLOWED  (training)
  OAI-SearchBot..... ALLOWED  (citation)
  PerplexityBot..... BLOCKED  (citation)   <- you are invisible in Perplexity
  ...
Summary: 1 blocked, 9 allowed  |  citation bots blocked: 1
```

## Methodology

- **Sample:** 41 widely-used AI and SaaS tools across writing, design, video, SEO, productivity, CRM, and the major AI labs.
- **Source:** each tool's **live, public `robots.txt`** fetched in June 2026.
- **Parsing:** longest-match `User-agent` resolution; a path is "blocked" for a bot if the effective rule set disallows `/`. A `User-agent: *` `Disallow: /` counts as blocking every bot; a specific allow for a bot overrides it.
- **Caveat:** `robots.txt` is a *request*, not enforcement, and sites change it over time. This is a point-in-time snapshot. Re-run the script any time to refresh.

## Reproduce / refresh the data

The dataset is a plain snapshot. To rebuild it for today, run `check_robots.py` across the domains in `data/ai-crawler-blocklist.csv` and re-tally. PRs that add tools or refresh the snapshot are welcome.

## Source & free tools

This dataset powers a free, no-signup web tool and a full write-up:

- **Full study (charts + analysis):** https://aitoolsinsiderhq.com/ai-crawler-study.html
- **Free AI Crawler & robots.txt Access Checker** (paste your robots.txt, see which AI bots you allow/block): https://aitoolsinsiderhq.com/ai-crawler-access-checker.html
- **Free llms.txt generator** (the "robots.txt for AI"): https://aitoolsinsiderhq.com/llms-txt-generator.html

Built by **[AI Tools Insider](https://aitoolsinsiderhq.com)** — AI tools, tested honestly.

## License

- **Code** (`check_robots.py`): MIT — see `LICENSE`.
- **Data** (`data/*`): **CC BY 4.0**. Use it anywhere, including commercially. Please credit *AI Tools Insider* with a link to https://aitoolsinsiderhq.com/ai-crawler-study.html.

## Cite this dataset

> AI Tools Insider (2026). *AI Crawler Block List 2026: which AI crawlers the top 41 AI & SaaS tools block.* https://aitoolsinsiderhq.com/ai-crawler-study.html
