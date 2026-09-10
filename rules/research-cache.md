# Rule: Research Cache

Apply before **any** costly external lookup — patent queries, web searches, API
fetches, legacy-code sweeps, analytics pulls. External calls cost tokens, time,
and rate-limit budget. A result already on disk costs one Read.

## The cache is `docs/`

```
docs/
  <topic-slug>/
    <artifact>.md        <- research output, with a provenance header (below)
    <artifact>.json      <- raw payloads when the shape matters
```

`docs/` is **gitignored** — it is a local working cache, not a deliverable. It may
hold personal or account-scoped data (exports with emails, tokens, internal IDs),
so it must never be committed. Deliverables belong in `_agent_context/wiki/` or a
task's `_factory/<task-id>/output/`, which *are* tracked.

`<topic-slug>` is kebab-case and names the subject, not the tool:
`mrna-lipid-nanoparticle`, not `patents-run-3`. A future reader searches by
subject, and tool-named folders make the same subject unfindable twice.

## Check before you fetch

1. `Glob docs/**/*` — one call, shows every cached topic and artifact at once. Glob
   all extensions, not just `*.md`: raw `.json` payloads and exports live here too.
2. If a slug looks related, Read it. Check its provenance header (below) for
   `query`, `retrieved`, and `scope` before trusting the body.
3. Decide, in this order:
   - **Hit, fresh, scope covers the question** → use it. Do not re-fetch. Say so
     when reporting: "from cached research, retrieved <date>".
   - **Hit, but `scope` is narrower than the question** (cache has page 1, you need
     page 2; cache covers US, you need EP) → fetch only the gap, then extend the
     existing file. Do not re-run the part you already have.
   - **Hit, but stale** → re-fetch, then update the file (see "Writing back").
   - **Miss** → fetch, then write the result into `docs/<topic-slug>/`.

Skipping step 1 because "it probably isn't cached" is the failure this rule exists
to prevent. One Glob is cheaper than one WebFetch, always.

## Staleness

Judgment call, but anchor it to how fast the source actually moves:

| Source | Treat as fresh for | Why |
|---|---|---|
| Granted patents, published papers, standards | Indefinitely | The document does not change once published |
| Patent search *result sets* (counts, new filings) | ~30 days | New filings enter continuously; counts drift |
| Product docs, API references, pricing | ~7 days | Vendors ship changes without notice |
| Analytics / usage exports | Until the period of interest closes | A partial-period export is wrong, not just old |
| Anything the user calls "current" or "latest" | Re-fetch | The word is a freshness requirement |

When reusing something past its window, do not quietly rely on it — say the age
out loud and let the user decide: "cached 2026-04-02, ~5 months old — reuse or
re-fetch?"

## Writing back

Every cached artifact opens with a provenance header. Without it the file is
unjudgeable and the next agent re-fetches anyway, defeating the cache:

```markdown
---
topic: mrna-lipid-nanoparticle
question: Who is filing LNP delivery patents since 2020?
source: patents.google.com/xhr/query
query: q="mRNA lipid nanoparticle" after=priority:20200101
retrieved: 2026-09-10
scope: page 1 only — 10 rows of 1,240 total matches
verified: US11318199B2 spot-checked against its patent page; other rows from search response only
---
```

- `scope` is the field that makes partial results safe to reuse. State plainly what
  is *not* in the file — pages not fetched, jurisdictions excluded, rows unverified.
- `verified` carries forward what was actually confirmed. A later reader must not
  promote unverified search-response rows into stated fact.
- `retrieved` is an absolute date, never "today" or "last week".

**Never overwrite a cached file silently.** If the target exists, either extend it
(append a new dated section, keep the old one) or ask the user before replacing.
Losing prior research to a re-run is worse than a slightly messy file.

## Reporting to the user

Always say where a fact came from — a fresh call or the cache:

> Found 3 relevant filings. Two from cached research (`docs/mrna-lipid-nanoparticle/`,
> retrieved 2026-08-14); the third from a new query just now covering EP, which the
> cache did not include.

Presenting cached data as a fresh result is a correctness problem, not a style one:
the user may be making a decision that depends on the data being current.
