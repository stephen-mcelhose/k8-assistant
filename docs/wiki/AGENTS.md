# Wiki Schema

This wiki is maintained by an LLM using the llm-wiki skill
(https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Domain

Knowledge base for the **k8s-assistant** csgdaa-code skill. Covers:

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

1. `WebFetch` the tutorial URL
2. Discuss key takeaways (in chat) before writing anything
3. Write raw source to `docs/wiki/raw/tutorials/<slug>.md` (immutable)
4. Write wiki page to `docs/wiki/<slug>.md` with OKF frontmatter, synthesis, Key Commands, Prerequisites, Cross-references, Sources
5. Propagate — update any existing pages that cover the same topics (add wikilinks, new sections, updated claims)
6. Update `index.md` (new row) and append to `log.md`
7. **Lint** — run a full lint pass immediately after each ingest:
   - Check OKF frontmatter on all pages
   - Check index.md has every page
   - Check for orphans (no inbound wikilinks)
   - Check for missing cross-references to newly ingested page
   - Note forward-refs (wikilinks to not-yet-ingested pages) as ADVISORY — do not remove them
   - Fix real issues; append lint entry to `log.md`
8. Confirm with user before moving to the next tutorial
9. Commit after each full batch completes

### Forward-ref policy

Wikilinks to tutorials not yet ingested (e.g., `[[scale-app]]` before Tutorial #5 is ingested) are **expected and correct**. Flag them in the lint report as *"pending ingest"* — never remove or stub them out. They will resolve naturally as ingestion progresses.

## Raw Sources

Raw source files live in `docs/wiki/raw/`. They are immutable — the LLM reads them but never writes to them.

Planned raw sources:
- `raw/tutorials/` — one file per kubernetes.io tutorial (fetched by the sync plan)
- `raw/pr-notes.md` → `docs/pr-notes.md` (original analysis from csgdaa-skills PR #16)

## index.md

Structured catalog of all wiki pages. Updated on every write operation.

## log.md

Append-only chronological log. Format: `## [YYYY-MM-DD] operation | detail`
