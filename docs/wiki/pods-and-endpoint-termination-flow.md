---
type: concept
title: Explore Termination Behavior for Pods and Endpoints
description: How Pod termination interacts with EndpointSlice conditions (ready/serving/terminating), why terminating endpoints remain serving for connection draining, and how to configure terminationGracePeriodSeconds and preStop hooks.
resource: https://kubernetes.io/docs/tutorials/services/pods-and-endpoint-termination-flow/
tags: [termination, graceful-shutdown, endpointslice, preStop, lifecycle, connection-draining, service]
timestamp: 2026-08-07T00:00:00Z
---

# Explore Termination Behavior for Pods and Endpoints

This short tutorial makes the Pod termination lifecycle observable by watching EndpointSlice conditions change in real time. It explains the three-condition model on endpoints and why it matters for connection draining.

## The termination flow

When a Pod is deleted (by a rolling update, manual `kubectl delete pod`, or scale-down), the following sequence occurs:

1. Pod enters `Terminating` status; a replacement Pod is scheduled if the Deployment desired count requires it
2. The terminating Pod's endpoint in the EndpointSlice transitions from `{ready: true, serving: true, terminating: false}` to **`{ready: false, serving: true, terminating: true}`**
3. The replacement Pod's endpoint appears as `{ready: true, serving: true, terminating: false}` once it passes readiness checks
4. The terminating Pod's `preStop` hook runs; then SIGTERM is sent to the container; the kubelet waits up to `terminationGracePeriodSeconds` for the container to exit; SIGKILL is sent if it doesn't
5. When the Pod is fully gone, its endpoint entry is removed from the EndpointSlice

## The three endpoint conditions

| Condition     | Meaning |
|---------------|---------|
| `ready`       | Pod passed readiness probe and is not terminating. Set to `false` for terminating endpoints for **backward compatibility** — older load balancers that only check `ready` will stop sending new traffic |
| `serving`     | Pod can still serve requests. Remains `true` while the Pod is terminating but processing active connections. Load balancers that support connection draining should use this condition |
| `terminating` | Pod has been asked to terminate. Once true, will not revert to false |

**The key insight:** `ready: false` stops new traffic from reaching the terminating Pod (backward-compatible behaviour). `serving: true` signals to drain-aware load balancers that the Pod is still handling in-flight requests. This two-signal design lets smart clients implement graceful connection draining without breaking dumb clients.

## The demo manifest

The tutorial uses `terminationGracePeriodSeconds: 120` plus a `preStop` hook that `sleep 180` (longer than the grace period, so the container is eventually SIGKILL'd). This exaggerates the terminating window to make observation easier — in production, set the grace period to match your app's actual shutdown time.

## Key Commands

```bash
# Deploy nginx with long grace period and preStop hook
kubectl apply -f pod-with-graceful-termination.yaml
kubectl apply -f explore-graceful-termination-nginx.yaml

# Observe the EndpointSlice (one endpoint, ready: true)
kubectl get endpointslice
kubectl get endpointslices -o json -l kubernetes.io/service-name=nginx-service

# Trigger Pod termination
kubectl delete pod <nginx-pod-name>

# Watch replacement Pod appear and old Pod terminate
kubectl get pods

# Observe endpoint conditions during transition:
# Old endpoint: ready: false, serving: true, terminating: true
# New endpoint: ready: true, serving: true, terminating: false
kubectl get endpointslice -o json nginx-service-<hash>
```

## Prerequisites

- A running Deployment with a Service — e.g., from [[connect-applications-service]]
- Basic understanding of EndpointSlices and Services

## Key Concepts

- **`terminationGracePeriodSeconds`**: how long the kubelet waits after SIGTERM before sending SIGKILL; default 30s; set higher for apps that need time to flush/drain
- **`lifecycle.preStop`**: hook that runs before SIGTERM; useful for deregistering from service discovery or waiting for in-flight requests; counts against `terminationGracePeriodSeconds`
- **`serving` vs `ready` endpoint condition**: `serving` stays true during graceful shutdown; `ready` goes false immediately for backward compatibility; drain-aware LBs should watch `serving`
- **EndpointSlice**: the object tracking live endpoint IPs and their conditions; replaces the older Endpoints API; auto-updated by the endpoint controller as Pods come and go

## Cross-references

- [[connect-applications-service]] — EndpointSlices and Service networking fundamentals
- [[expose-app]] — Service concepts; why Pods behind a Service need graceful shutdown
- [[update-app]] — rolling updates trigger the same termination flow for each replaced Pod
- [[kubernetes-topic-taxonomy]] — `termination`, `graceful-shutdown`, `endpointslice`, `lifecycle` domains

## Sources

- `docs/wiki/raw/tutorials/pods-and-endpoint-termination-flow.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/services/pods-and-endpoint-termination-flow/
