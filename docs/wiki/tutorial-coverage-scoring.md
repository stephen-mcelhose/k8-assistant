---
type: concept
title: Tutorial Coverage Scoring
description: The context score formula used to rank kubernetes.io tutorials by how completable they are given the quick-reference guide as pre-existing context, and how the skill uses scores to sequence learning.
resource: references/tutorial-map.md
tags: [tutorials, scoring, pedagogy, context-score, sequencing]
timestamp: 2026-08-07T15:39:38Z
---

# Tutorial Coverage Scoring

The `references/tutorial-map.md` file assigns each of the 26 official kubernetes.io tutorials a **Context Score** — a principled measure of how likely a learner is to successfully complete that tutorial given the `quick-reference.md` as their only pre-existing context.

## Formula

```
Context Score = (Quick Ref Coverage × Tutorial Quality × (6 - Task Difficulty)) / 25
```

| Factor              | Scale | Meaning                                                              |
|---------------------|-------|----------------------------------------------------------------------|
| Quick Ref Coverage  | 1–5   | How much of the tutorial's content is covered by quick-reference.md  |
| Tutorial Quality    | 1–5   | Quality of the official kubernetes.io tutorial itself                |
| Task Difficulty     | 1–5   | How hard the tutorial is (inverted: easier = higher score)           |

**Maximum possible score**: `(5 × 5 × 5) / 25 = 5.0`

## Score distribution across the 26 tutorials

| Score range | Tutorials | Interpretation                                    |
|-------------|-----------|---------------------------------------------------|
| 3.5–4.0     | 4         | Ideal starting points — high coverage, easy wins  |
| 2.5–3.4     | 8         | Good mid-range — solid reference overlap          |
| 1.5–2.4     | 9         | Moderate — learner will need to go beyond the ref |
| 0.5–1.4     | 5         | Advanced — minimal reference support available    |

Top-scoring tutorials (score ≥ 3.5): **[[deploy-app|Deploy an App]]** (4.0), **[[explore-app|Explore Your App]]** (4.0), **[[scale-app|Scale Up Your App]]** (4.0), **[[namespaces-walkthrough|Namespaces Walkthrough]]** (3.2), **[[expose-external-ip|Exposing External IP]]** (3.2).

## How the skill uses this

In `## Objective Setting`, the skill reads `references/tutorial-map.md` and finds the module with the highest Context Score that also matches the tags from the user's question (see [[kubernetes-topic-taxonomy]]). High-scoring tutorials are preferred as starting points; lower-scoring ones are suggested once the learner has built more context.

This is intentional sequencing: beginners land on [[deploy-app|Deploy]], [[explore-app|Explore]], and [[scale-app|Scale]] first (score 4.0), then progress toward StatefulSets, security hardening, and DRA as their reference knowledge grows.

## Limitations

- The formula assumes `quick-reference.md` is the only pre-existing context. A learner with prior k8s experience should be steered differently.
- "Tutorial Quality" is a static score from the original analysis — it doesn't update when kubernetes.io revises a tutorial.
- Tag matching is fuzzy: the skill does not currently do exact tag lookup, it relies on the agent's judgment when reading the table. See [[tutorial-sync-plan]] for how this could be tightened via wiki ingestion.

## Sources

- `references/tutorial-map.md` — full scored table of 26 tutorials
- `docs/pr-notes.md` — formula and scoring rationale from PR #16 analysis
