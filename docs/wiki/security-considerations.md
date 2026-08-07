---
type: concept
title: Security Considerations
description: Known security surface of the k8s-assistant skill — credential exposure risk from kubectl config view, and design notes on the allowed-tools boundary.
resource: docs/pr-notes.md
tags: [security, kubectl, credentials, allowed-tools, kubeconfig]
timestamp: 2026-08-07T15:39:38Z
---

# Security Considerations

The k8s-assistant has a low overall security risk (SkillSpector score 17/100, severity LOW), but two findings are worth tracking actively.

## SQP-2 — Credential exposure via `kubectl config view` (MEDIUM)

**Location**: `SKILL.md` allowed-tools list — `Bash(kubectl config view:*)`

`kubectl config view` outputs the full kubeconfig, which routinely contains:
- Cluster API server addresses
- Client certificate data
- Bearer tokens
- Base64-encoded credentials

If the agent runs this command and surfaces the output in a chat or log (especially a shared/recorded session), credentials sufficient to authenticate to the cluster can be exposed.

**Current status**: The allowed-tools list still includes `kubectl config view`. The skill's `## Environment Discovery` step uses it to identify the cluster context.

**Mitigations to consider**:
1. Replace `kubectl config view` with `kubectl config current-context` + `kubectl config get-contexts` — these show context names and cluster labels without exposing credential data.
2. If `kubectl config view` is retained, add an explicit agent instruction to redact `client-certificate-data`, `token`, and `password` fields before surfacing output.
3. Document in the skill description that cluster credentials may be accessed (allows operators to make an informed decision before deploying).

See [[skill-design-principles]] for the Environment Discovery step where this is used.

## SDI-4 — Mislabelled read-only restriction (LOW, resolved)

The original skill (csgdaa-skills PR #16) labelled itself "Read-Only" in the skill body but allowed write command suggestions. This created a false sense of security. **Resolved**: the read-only label and restrictions have been removed from this fork. The skill now has full kubectl access, which is honest about its actual capability.

## Allowed-tools surface

The current allowed-tools list covers:

| Category       | Commands                                                            |
|----------------|---------------------------------------------------------------------|
| Read           | `get`, `describe`, `logs`, `top`, `explain`, `auth can-i`          |
| Config         | `config view`, `config get-contexts`, `config current-context`, `config use-context`, `cluster-info` |
| Write          | `apply`, `create`, `delete`, `edit`, `patch`, `scale`, `rollout`, `expose`, `run` |
| Filesystem     | `ls`, `Read`, `Glob`, `Grep`                                       |

The csgdaa-code automated review (Grade A) noted the granular verb-level scoping as a strong pattern. The `Bash(ls:*)` entry could be replaced with `Glob` if surface area reduction is desired.

## Sources

- `docs/pr-notes.md` — SkillSpector scan results and remediation notes from PR #16
