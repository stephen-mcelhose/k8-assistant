---
type: concept
title: Apply Pod Security Standards at the Namespace Level
description: How to enforce, warn, and audit Pod Security Standards on a per-namespace basis using namespace labels, demonstrated with kind and the baseline/restricted PSS levels.
resource: https://kubernetes.io/docs/tutorials/security/ns-level-pss/
tags: [pod-security, namespace, pss, baseline, restricted, admission-controller, kind, labels]
timestamp: 2026-08-07T00:00:00Z
---

# Apply Pod Security Standards at the Namespace Level

**Pod Security Admission** is a built-in admission controller (GA in v1.25) that enforces **Pod Security Standards** (PSS) when Pods are created. Rather than cluster-wide policy, this tutorial applies PSS one namespace at a time via namespace labels — giving teams different security postures in different namespaces.

There are three PSS levels: **privileged** (unrestricted), **baseline** (minimal restrictions, blocks known privilege escalation), and **restricted** (hardened — requires non-root, drops capabilities, sets seccomp). Each level can be applied in three independent modes via namespace labels: **enforce** (blocks non-compliant Pods), **warn** (allows creation but prints a client-side warning), and **audit** (records to the audit log, silent to the user). A namespace can carry all three modes simultaneously, at different levels.

The tutorial creates a `kind` cluster, then labels the `example` namespace to enforce `baseline` while warning and auditing against `restricted`. When a baseline-compliant Pod is created in `example`, it starts successfully but prints a warning listing the `restricted` violations (no `allowPrivilegeEscalation=false`, no capabilities drop, etc.). The same Pod created in `default` (no PSS labels) produces no warnings — demonstrating that PSS only applies where the labels exist.

**Key insight:** PSS enforcement is opt-in per namespace. New namespaces have no policy by default. Cluster-level defaults can be set separately (see `cluster-level-pss`).

## Key Commands

```bash
# Create a kind cluster for this tutorial
kind create cluster --name psa-ns-level
kubectl cluster-info --context kind-psa-ns-level

# Create and label a namespace
kubectl create ns example

# Warn-only on baseline (single mode, single label pair)
kubectl label --overwrite ns example \
  pod-security.kubernetes.io/warn=baseline \
  pod-security.kubernetes.io/warn-version=latest

# Enforce baseline, warn + audit restricted (all three modes)
kubectl label --overwrite ns example \
  pod-security.kubernetes.io/enforce=baseline \
  pod-security.kubernetes.io/enforce-version=latest \
  pod-security.kubernetes.io/warn=restricted \
  pod-security.kubernetes.io/warn-version=latest \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/audit-version=latest

# Create a baseline-compliant Pod in the labeled namespace
# → succeeds, but prints warning about restricted violations
kubectl apply -n example -f https://k8s.io/examples/security/example-baseline-pod.yaml

# Same Pod in default namespace → no warnings (no PSS labels)
kubectl apply -n default -f https://k8s.io/examples/security/example-baseline-pod.yaml

# Cleanup
kind delete cluster --name psa-ns-level
```

## Prerequisites

- `kind` installed on the workstation
- `kubectl` installed
- Kubernetes v1.25+ (Pod Security Admission is GA)

## Key Concepts

- **Pod Security Standards (PSS)**: three policy levels — `privileged`, `baseline`, `restricted`; defined by the Kubernetes project, not configurable per-cluster
- **Pod Security Admission**: the built-in admission controller that enforces PSS; replaces the deprecated PodSecurityPolicy
- **Enforcement modes**: `enforce` blocks, `warn` warns the client, `audit` records to audit log — each independently set via namespace labels
- **`-version` label**: pins the PSS check to a Kubernetes version's definition (use `latest` or a specific version like `v1.25`); prevents policy drift on cluster upgrade
- **Namespace-scoped**: PSS labels only affect the namespace they are on; other namespaces are unaffected
- **Warning format**: when `warn` mode fires, kubectl prints the violation details before confirming creation — useful for assessing impact before enforcing

## Cross-references

- [[namespaces-walkthrough]] — namespace creation and isolation fundamentals
- [[kubernetes-topic-taxonomy]] — `pod-security`, `namespace`, `admission-controller` domains

## Sources

- `docs/wiki/raw/tutorials/ns-level-pss.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/security/ns-level-pss/
