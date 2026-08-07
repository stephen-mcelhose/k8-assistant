# ADR-0001: Wiki ingestion scope

**Date:** 2026-08-07  
**Status:** Accepted  
**Authors:** stephen.mcelhose.ext

---

## Context

The k8-assistant skill uses a local wiki as a retrieval index — pages are surfaced to the LLM at query time to provide precise kubectl commands, flags, and workflows. We needed to decide which parts of the kubernetes.io documentation corpus to ingest.

The key constraint: the skill is **kubectl-focused**, targeting the advanced-beginner to competent range of the Dreyfus model. It is not a general Kubernetes education system.

A secondary consideration: LLM knowledge of Kubernetes has matured significantly since the skill was first built (~7 months ago). Things that previously required wiki context are now free from model knowledge.

---

## Decision

### Ingest

| Source | Rationale |
|--------|-----------|
| **All 26 kubernetes.io tutorials** | Direct 1:1 mapping to kubectl skill progression; exact commands and flags that require precise retrieval |
| **kubectl Quick Reference** (`/docs/reference/kubectl/quick-reference/`) | Canonical command cheat sheet; complements tutorials with flag details and JSONPath/output-format reference |
| **Manual tag taxonomy** (PR #16 comment) | Authoritative vocabulary for retrieval matching; 30 categories, ~200 tags |

### Do not ingest

| Source | Reason |
|--------|--------|
| **Concepts section** | LLM already knows Kubernetes architecture and resource semantics; ingesting adds retrieval noise without new signal |
| **Getting Started / Production setup** | Cluster admin and provisioning focus; outside the skill's kubectl scope |
| **Tasks section** | Broad and noisy; majority is cluster admin (TLS rotation, network policy providers, kubeadm administration); the few kubectl-relevant tasks are covered by tutorials |
| **Reference > Well-Known Labels, Annotations and Taints** | 102K-character page; ~10 of ~100+ entries are useful to a kubectl learner; LLM already knows all 10; rest is internal controller annotations, deprecated fields, and simulator tooling |
| **Supplemental tutorial scoring analysis** | Author-noted "numbers made up"; directionally useful but not authoritative reference material |
| **Glossary** | Definitional content the LLM holds natively; no retrieval benefit |

---

## Consequences

- Wiki stays narrow and high signal-to-noise: 31 pages, all directly actionable
- Retrieval queries return relevant kubectl context rather than conceptual or admin noise
- If the skill expands scope (e.g. cluster administration, RBAC deep-dive), ingestion scope should be revisited per this ADR
- The `log.md` file in `docs/wiki/` records individual ingestion events; this ADR records the *why* behind what was included and excluded

---

## Revisit triggers

- Skill scope expands beyond kubectl to cover cluster administration or security hardening
- A user scenario arises that the current wiki demonstrably cannot handle and the LLM cannot fill from its own knowledge
- kubernetes.io significantly restructures its tutorial content
