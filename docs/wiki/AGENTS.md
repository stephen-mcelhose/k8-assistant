# Wiki Schema

This wiki is maintained by an LLM using the llm-wiki skill
(https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Domain

Knowledge base for the **k8s-assistant** skill. Covers:

- Kubernetes concepts, resources, and kubectl commands (from official kubernetes.io tutorials)
- Skill design principles — how the assistant is structured, its pedagogical approach, security surface
- Tutorial coverage analysis — which tutorials are best suited for which learners
- Topic taxonomy — the canonical tag vocabulary used for indexing and tutorial matching

The primary consumers are:
1. The k8s-assistant skill itself (as enriched reference material)
2. Maintainers improving the skill or adding new tutorials

## Conventions

- **Page slugs**: kebab-case (e.g., `kubernetes-networking.md`)
- **Frontmatter**: OKF — `type` (default `concept`), `title`, `description`, `timestamp` (ISO-8601 UTC); optional `resource`, `tags`
- **Cross-references**: `[[Page Slug]]` wikilinks
- **Sources section**: every page ends with `## Sources` listing its raw inputs

## Operations

Run these via the `llm-wiki` skill from within `~/repos/k8-assistant`:

- `ingest <source>` — read a new source, write a summary page, propagate to related pages
- `query <question>` — synthesize an answer from wiki pages, optionally write back
- `lint` — audit for orphans, contradictions, stale claims, missing links

## Ingest workflow (tutorial batch ingestion)

For each tutorial ingest from `docs/wiki/tutorial-sync-plan.md`, follow this sequence:

1. **Fetch verbatim source** — `curl -s <URL>` to a temp file, then run the extraction
   script (`tools/extract.py`) to pull the `<main data-pagefind-body>` element,
   strip all HTML tags and inline scripts, and write plain text to
   `docs/wiki/raw/tutorials/<slug>.md` with an attribution header.
   This is the **only** write to `raw/` — it is immutable after this step.
   Do NOT use WebFetch for raw files; WebFetch is an AI summariser, not a verbatim fetcher.
2. **Read the raw file** — Read `docs/wiki/raw/tutorials/<slug>.md` to understand the
   full source content before writing anything else.
3. **Discuss key takeaways** — surface 3–5 key ideas in chat for the user to redirect if needed.
4. **Write wiki page** — `docs/wiki/<slug>.md` with OKF frontmatter, synthesis,
   Key Commands, Prerequisites, Cross-references, Sources.
   Synthesise from the raw file, not from memory or WebFetch output.
5. **Propagate** — update any existing pages that cover the same topics.
6. **Update `index.md`** (new row) and append to `log.md`.
7. **Lint** — full lint pass immediately after each ingest:
   - Check OKF frontmatter on all pages
   - Check index.md has every page
   - Check for orphans (no inbound wikilinks)
   - Check for missing cross-references to newly ingested page
   - Note forward-refs (wikilinks to not-yet-ingested pages) as ADVISORY — do not remove them
   - Fix real issues; append lint entry to `log.md`
8. **Confirm** with user before moving to the next tutorial.
9. **Commit** after each full batch completes.

### Forward-ref policy

Wikilinks to tutorials not yet ingested (e.g., `[[scale-app]]` before Tutorial #5 is ingested)
are **expected and correct**. Flag them in the lint report as *"pending ingest"* — never remove
or stub them out. They will resolve naturally as ingestion progresses.

### Miss-rate baseline

A miss rate check (word coverage of raw vs. actual page) should read **~0%** for raw files,
since they are verbatim extractions. The wiki page synthesises from raw and will naturally
have lower coverage — that is intentional and acceptable.

## Raw Sources

Raw source files live in `docs/wiki/raw/`. They are **immutable verbatim extractions** —
plain text of the `<main>` content from the source page, tags stripped, no summarisation.
The LLM reads them; it never rewrites them.

License: kubernetes.io documentation is published under **CC BY 4.0**. Raw files include
an attribution header with the source URL and fetch date. See `docs/wiki/raw/LICENSE-raw.md`.

Planned raw sources:
- `raw/tutorials/` — one file per kubernetes.io tutorial (fetched by the sync plan)
- `tools/extract.py` — reusable extraction script: curl → strip tags → write attribution header
- `raw/manual/` — manually authored reference files (tag taxonomy, etc.)

**Version control**: raw files are committed to git to enable the quarterly diff/sync
strategy (re-fetch → diff against stored snapshot → re-ingest if changed). A
`.gitattributes` entry marks `docs/wiki/raw/tutorials/` as `linguist-generated=true`
so GitHub does not count them as authored code.

## index.md

Structured catalog of all wiki pages. Updated on every write operation.

## log.md

Append-only chronological log. Format: `## [YYYY-MM-DD] operation | detail`
