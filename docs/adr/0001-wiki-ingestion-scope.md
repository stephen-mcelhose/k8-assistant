---
type: decision
title: Wiki ingestion scope
description: Limits wiki ingestion to the 26 kubernetes.io tutorials and the kubectl quick-reference, excluding Concepts, Tasks, and Reference sections whose signal is already free in the LLM.
resource: https://kubernetes.io/docs/home/
tags: [wiki, ingestion, kubectl, kubernetes, retrieval]
timestamp: 2026-08-07T18:28:56Z
---

# Wiki ingestion scope

## Status

`accepted`

## Y-Statement

In the context of **building a retrieval index for a kubectl-focused learning skill**,
facing **a large kubernetes.io documentation corpus with high noise-to-signal ratio outside the tutorials section, and LLMs that now hold strong baseline Kubernetes knowledge natively**,
we decided **to ingest only the 26 official tutorials, the kubectl quick-reference, and a manually curated tag taxonomy**,
to achieve **a narrow, high-signal wiki where retrieval surfaces actionable kubectl commands rather than conceptual or administrative noise**,
accepting **coverage gaps for topics not covered by the tutorials (e.g. resource limits, advanced RBAC), which the LLM's own knowledge must fill at query time**.

## Context and Problem Statement

The k8-assistant skill uses a local wiki as a retrieval index. Pages are surfaced to the LLM at query time to provide precise kubectl syntax, flags, and workflows. With the full kubernetes.io docs available (~6 major sections, hundreds of pages), we needed a principled answer to: *what belongs in the wiki?*

The skill targets the advanced-beginner to competent range of the Dreyfus model, with kubectl as the primary subject. When the skill was originally built (~7 months prior), LLM Kubernetes knowledge was shallower and wiki coverage mattered more. By the time of this decision, most conceptual and architectural Kubernetes knowledge is effectively free from the model.

## Decision Drivers

- Retrieval noise degrades answer quality — more pages means a higher chance of surfacing the wrong context
- The skill is kubectl-scoped, not a general Kubernetes education system
- LLM baseline knowledge has matured; ingesting content the model already knows adds cost without benefit
- Maintenance overhead scales with corpus size

## Considered Options

- **Option A:** Ingest tutorials + quick-reference only *(chosen)*
- **Option B:** Ingest tutorials + Concepts section
- **Option C:** Ingest tutorials + selected Tasks pages
- **Option D:** Ingest tutorials + Reference > Well-Known Labels, Annotations and Taints
- **Option E:** Broad ingestion across all six sections

## Decision Outcome

Chosen option: **Option A — tutorials + quick-reference + tag taxonomy**, because the tutorials directly map 1:1 to kubectl skill progression, the quick-reference fills the flag/syntax gap, and everything else either duplicates LLM knowledge or introduces retrieval noise.

### Consequences

- **Good:** wiki stays at 31 pages, all directly actionable; retrieval queries return relevant kubectl context
- **Good:** low maintenance burden; fewer pages to update when kubernetes.io changes
- **Bad:** the wiki cannot answer questions outside the tutorials (e.g. "how do I set CPU limits?"); the LLM fills this gap from its own knowledge, which is unverifiable and may drift
- **Bad:** if the skill scope expands to cluster administration, the wiki will need a deliberate extension

### Pros and Cons of the Options

#### Option B — add Concepts section

- Good, because conceptual depth supports "why" questions alongside "how" questions
- Bad, because the LLM already knows Kubernetes concepts; ingesting adds retrieval noise without new signal

#### Option C — add selected Tasks pages

- Good, because Tasks fills real gaps (resource limits, probes, secrets patterns)
- Bad, because the Tasks section is broad and noisy; majority is cluster admin (TLS rotation, network policy providers, kubeadm); the filtering burden is high and ongoing

#### Option D — add Well-Known Labels, Annotations and Taints

- Good, because labels like `app.kubernetes.io/*` and `topology.kubernetes.io/zone` are commonly used with `kubectl label`
- Bad, because the page is 102K characters; roughly 10 of 100+ entries are useful to a kubectl learner; the rest is internal controller annotations, deprecated fields, and simulator tooling; the LLM already knows all 10 useful ones

#### Option E — broad ingestion

- Good, because maximum coverage
- Bad, because retrieval precision collapses; not kubectl-scoped; maintenance is unsustainable

## More Information

- `docs/wiki/log.md` — records individual ingestion events with dates
- `docs/wiki/index.md` — current wiki page inventory
- `docs/wiki/kubernetes-topic-taxonomy.md` — tag vocabulary used for retrieval matching

**Revisit triggers:**
- Skill scope expands beyond kubectl (cluster admin, security hardening, RBAC deep-dive)
- A recurring user scenario arises that neither the wiki nor the LLM can handle reliably
- kubernetes.io significantly restructures its tutorial section
