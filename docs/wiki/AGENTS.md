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

## Raw Sources

Raw source files live in `docs/wiki/raw/`. They are immutable — the LLM reads them but never writes to them.

Planned raw sources:
- `raw/tutorials/` — one file per kubernetes.io tutorial (fetched by the sync plan)
- `raw/pr-notes.md` → `docs/pr-notes.md` (original analysis from csgdaa-skills PR #16)

## index.md

Structured catalog of all wiki pages. Updated on every write operation.

## log.md

Append-only chronological log. Format: `## [YYYY-MM-DD] operation | detail`
