# Google Patents Search Skill

Domain knowledge for querying patents.google.com via WebFetch — reliably, with the
fewest possible calls. No dedicated agent needed for this; any agent (or the
orchestrator itself) can self-load this file before a patent lookup.

---

## Core problem

`patents.google.com/?q=...` is a client-rendered SPA. WebFetch converts HTML to
Markdown and does not execute JavaScript, so fetching the search UI URL directly
returns an empty page shell with no results.

**Never fetch the search UI URL for results.** Use the internal JSON endpoint instead:

```
https://patents.google.com/xhr/query?url=<url-encoded-query-params>&exp=&content=1
```

This is an undocumented endpoint the search UI itself calls — treat it as
lightweight/best-effort, not a stable public API. Fine for occasional lookups;
do not build high-volume automated harvesting on top of it.

---

## Building the query

The `url` param value is the same query string the search bar would produce,
URL-encoded as a whole. Common fields:

| Field | Example | Meaning |
|---|---|---|
| `q=` | `q=%22mRNA+lipid+nanoparticle%22` | Keywords — quote multi-word phrases |
| `after=priority:` / `before=priority:` | `after=priority:20200101` | Priority date range (YYYYMMDD) |
| `after=filing:` / `before=filing:` | `before=filing:20241231` | Filing date range |
| `after=publication:` / `before=publication:` | | Publication date range |
| `assignee=` | `assignee=Moderna` | Filter by assignee/applicant |
| `inventor=` | `inventor=Katalin+Karikó` | Filter by inventor |
| `country=` | `country=US,EP,CN` | Jurisdictions |
| `status=` | `status=GRANT` or `status=APPLICATION` | Grant status |
| `type=` | `type=PATENT` or `type=DESIGN` | Document type |

Full worked example (query: "mRNA lipid nanoparticle", priority 2020–2024):

```
https://patents.google.com/xhr/query?url=q%3D%22mRNA%2Blipid%2Bnanoparticle%22%26before%3Dpriority:20241231%26after%3Dpriority:20200101&exp=&content=1
```

Add `&page=1`, `&page=2`, … to the same URL for subsequent result pages.

---

## Minimal-cost fetch pattern

0. **Check the cache first** — `Glob docs/**/*`, and read any topic folder whose
   slug looks related. A prior lookup may already answer the question, or cover part
   of it (page 1 fetched, EP missing) so you only fetch the gap. This matters more
   here than for most sources: `xhr/query` rate-limits after a handful of rapid
   calls, so a cache hit protects the budget for the queries you genuinely need.
   Full protocol — freshness windows, provenance header, write-back — in
   `rules/research-cache.md`.
1. **One** WebFetch call to the `xhr/query` endpoint. Prompt it explicitly for a
   Markdown table with: title, publication number, assignee, priority (or filing)
   date — plus the total result count reported by the query. The total count tells
   you if the query is too broad/narrow before spending another call refining it.
2. Do **not** fetch a detail page per result. The search endpoint already returns
   title/assignee/dates for every row on the page — that's the data source, not a
   teaser.
3. Spot-check **one** result — not all — by fetching
   `https://patents.google.com/patent/<publication_number>/en` when the data will
   be relayed to the user as fact (not a draft) or when something looks off
   (implausible date, mismatched assignee). One confirmation validates that the
   extraction for that call is honest; it does not need repeating per row.
4. Only escalate to per-patent detail fetches when the user needs claims, full
   abstract text, citations, or legal-status detail — none of which the search
   endpoint returns.
5. Never call `xhr/query` once per desired result. One call returns a full page
   (typically 10 rows) — pick from that page rather than issuing N calls for N
   patents.
6. **Write the result back** to `docs/<topic-slug>/<artifact>.md` with the provenance
   header from `rules/research-cache.md`. Record the exact `url=` query string, the
   total match count, which page(s) you fetched, and which single row (if any) you
   spot-checked — that is what lets the next lookup reuse this instead of re-querying
   a rate-limited endpoint. Granted-patent data does not go stale; a *result set*
   does, so `retrieved` and `scope` are what a later reader judges freshness on.

---

## Known failure modes

| Symptom | Cause | Fix |
|---|---|---|
| WebFetch returns "no search results" / only a page header | Fetched the SPA URL (`/?q=...`) directly | Switch to `/xhr/query?url=...` |
| `WebSearch` tool throws a Bedrock/litellm `inputSchema is invalid` 400 error | Tool-level bug, unrelated to the query text | Do not retry `WebSearch` for this domain — go straight to `xhr/query` via `WebFetch` |
| Result list looks generic or numbers look suspiciously rounded | Summarization drift from the small model behind WebFetch | Re-issue the same WebFetch call asking for verbatim fields, or spot-check one item against its patent page |
| Query returns thousands of results dominated by irrelevant families | Missing date bounds or an unquoted multi-word phrase | Quote phrases (`%22...%22`), add `before=`/`after=priority`, add `assignee=` if a company is implied |
| Everything under a broad noun (e.g. "display", "network") returns the same company's UI/software filings regardless of how many extra keyword phrases are ORed in | A single generic word matches across a huge, unrelated portfolio (e.g. Apple's GUI/Vision Pro filings all contain "display") — adding more quoted phrases in the same `q=` widens the match (OR), it does not narrow it | Narrow via structural filters instead of more keywords: `cpc=<classification>` for the actual hardware art class, or accept the noise and manually pick the results whose title/snippet is genuinely on-topic rather than re-querying repeatedly |
| `xhr/query` starts returning `HTTP 503 Service Unavailable` after several calls in quick succession | Endpoint-side rate limiting — it's an internal, undocumented endpoint with no published quota | Stop iterating; space out requests. Get the query right on paper first (date bounds, assignee, phrase quoting) so one call suffices instead of narrowing through 4-5 rapid trial calls |

---

## Reporting results to the user

For each patent reported, include: title, publication number, assignee, priority
(or filing) date, and a direct link:

```
https://patents.google.com/patent/<publication_number>/en
```

Always state the total result count the query matched and whether what's shown
is the full result set or a sample. Note explicitly if only one row was verified
directly against its patent page — the rest came from the search response only.

---

## When this isn't the right tool

For bulk/programmatic access (thousands of patents, structured export, joins
across fields) point the user at **Google Patents Public Datasets on BigQuery**
instead of scaling this WebFetch pattern up — scraping the XHR endpoint at volume
risks rate-limiting and is not what it's designed for.
