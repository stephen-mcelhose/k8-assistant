---
type: concept
title: Adopting Sidecar Containers
description: How native sidecar containers (initContainers with restartPolicy Always, stable since v1.33) differ from legacy sidecars, their benefits for Jobs and startup ordering, and how to adopt them safely including 3rd-party tooling concerns.
resource: https://kubernetes.io/docs/tutorials/configuration/pod-sidecar-containers/
tags: [sidecar, init-containers, restart-policy, jobs, mutating-webhook, feature-gate, networking]
timestamp: 2026-08-07T00:00:00Z
---

# Adopting Sidecar Containers

A **native sidecar container** is an `initContainer` with `restartPolicy: Always`. This feature is stable from Kubernetes v1.33 (beta from v1.29, enabled by default). The concept of a sidecar (a helper container running alongside the main container) is not new — it was previously implemented as a regular container in the `containers` list. Native sidecars fix several fundamental limitations of that approach.

## Why native sidecars

The core problem with legacy sidecars (regular containers acting as sidecars) is lifecycle: the scheduler has no way to know which containers are primary and which are helpers. Native sidecars, by being declared as init containers with a restart policy, give the control plane explicit semantic knowledge:

- **Startup order**: a native sidecar starts before any regular `containers` (init container semantics)
- **Shutdown order**: sidecar receives SIGTERM only after all regular containers have finished; if it doesn't exit cleanly, it gets SIGKILL — guaranteed last to terminate
- **Jobs**: with `restartPolicy: OnFailure` or `Never`, a legacy sidecar blocks Job completion (the Pod never reaches Succeeded because the sidecar keeps running). Native sidecars do not block Job completion; they are terminated when regular containers finish

## Adoption considerations

The tutorial is primarily a migration guide for teams moving from legacy to native sidecars. Key challenges:

**Feature gate:** Verify the feature is enabled on both API server and all nodes (required v1.29+):
```bash
kubectl get --raw /metrics | grep kubernetes_feature_enabled | grep SidecarContainers
# Should show: kubernetes_feature_enabled{name="SidecarContainers",stage="STABLE"} 1
kubectl get --raw /api/v1/nodes/<node-name>/proxy/metrics | grep kubernetes_feature_enabled | grep SidecarContainers
```

**Mutating webhooks / 3rd-party tools:** Service mesh injectors and other admission webhooks may strip the `restartPolicy` field from init containers if they were built against a pre-v1.28 Kubernetes client library. The field is simply dropped silently. Verify by running `kubectl describe pod <pod>` after creation — if `restartPolicy: Always` is absent from the init container spec, a webhook is stripping it. The fix is to recompile the webhook/tool with v1.28+ API client code, or switch to patch-based mutation strategies that preserve unknown fields.

**Universal sidecar injector pattern:** For environments where node compatibility cannot be guaranteed, inject both a native sidecar (`initContainer` with `restartPolicy: Always`) and a legacy sidecar (regular container). The native sidecar writes a sentinel file on first start; the legacy sidecar checks for the sentinel and exits immediately if the native sidecar is running. This is wasteful (resources counted twice) but provides a safe transition path.

## Key Commands

```bash
# Check feature gate on API server
kubectl get --raw /metrics | grep kubernetes_feature_enabled | grep SidecarContainers

# Check feature gate on a specific node
kubectl get --raw /api/v1/nodes/<node-name>/proxy/metrics | grep kubernetes_feature_enabled | grep SidecarContainers

# Verify a sidecar pod spec preserved restartPolicy after admission
kubectl describe pod <pod-name>
# Look for: restartPolicy: Always in the initContainers section
```

## Native sidecar manifest pattern

```yaml
spec:
  initContainers:
  - name: my-sidecar
    image: my-sidecar-image
    restartPolicy: Always   # this is what makes it a native sidecar
    # ... ports, volumeMounts, etc.
  containers:
  - name: main-app
    image: main-app-image
```

## Prerequisites

- Kubernetes v1.29+ for beta (enabled by default); v1.33+ for stable
- Understanding of init containers and Pod lifecycle
- Relevant if using service meshes, log shippers, or any injected sidecar pattern

## Key Concepts

- **Native sidecar**: `initContainer` with `restartPolicy: Always` — starts before regular containers, terminates last, does not block Job completion
- **Legacy sidecar**: a regular container in `containers[]` used as a helper — no lifecycle guarantees, blocks Jobs
- **`restartPolicy: Always` on initContainer**: the only field that distinguishes a native sidecar from a regular init container; init containers without this field run to completion before main containers start
- **Mutating webhook risk**: webhooks built against pre-v1.28 API may silently drop `restartPolicy` — verify with `kubectl describe pod`
- **Feature gate check**: `kubernetes_feature_enabled{name="SidecarContainers",...} 1` confirms the feature is on

## Cross-references

- [[updating-configuration-via-a-configmap]] — uses a native sidecar in scenario 4
- [[guestbook]] — multi-container Pods with shared volumes (pre-sidecar pattern)
- [[configure-redis-configmap]] — `kubectl exec` into running containers
- [[kubernetes-topic-taxonomy]] — `sidecar`, `init-containers`, `mutating-webhook` domains

## Sources

- `docs/wiki/raw/tutorials/pod-sidecar-containers.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/configuration/pod-sidecar-containers/
