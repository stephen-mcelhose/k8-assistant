---
type: concept
title: StatefulSet Basics
description: Comprehensive walkthrough of StatefulSet create/delete/scale/update — stable Pod identity, ordered creation and deletion, PersistentVolumeClaim lifecycle, RollingUpdate with partitions, and cascading vs non-cascading delete.
resource: https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/
tags: [statefulset, pvc, headless-service, rolling-update, partition, scale, stable-identity, dns, ordered]
timestamp: 2026-08-07T00:00:00Z
---

# StatefulSet Basics

This is the definitive hands-on tutorial for StatefulSets. It covers the full lifecycle — create, inspect, scale, update, and delete — using a two-replica nginx StatefulSet backed by PersistentVolumeClaims. The tutorial requires dynamic PV provisioning and a default StorageClass.

## Core StatefulSet guarantees

Unlike Deployments (where Pod identity is ephemeral and interchangeable), a StatefulSet provides:

- **Stable, unique Pod names**: `<name>-<ordinal>` — e.g., `web-0`, `web-1`. Names persist across restarts.
- **Stable network identity**: each Pod gets a DNS entry `<pod-name>.<headless-service>.<namespace>.svc.cluster.local` (e.g., `web-0.nginx.default.svc.cluster.local`). The headless Service (`clusterIP: None`) enables this per-Pod DNS without a load-balanced VIP.
- **Stable persistent storage**: each Pod gets its own PVC via `volumeClaimTemplates`. PVCs survive Pod deletion and are remounted to the same ordinal Pod when it restarts. **PVCs are never deleted by the StatefulSet controller** — not on Pod deletion, not on scale-down, not on StatefulSet deletion. This is an explicit safety design.
- **Ordered operations**: creation goes 0→n-1 (each Pod must be Running+Ready before the next starts); deletion goes n-1→0 (reverse order, each fully terminated before the next starts).

## Updates

The default update strategy is `RollingUpdate` — updates in reverse ordinal order (n-1→0), one Pod at a time, waiting for Ready before proceeding.

**Partitioned rolling update**: set `spec.updateStrategy.rollingUpdate.partition=N` to update only Pods with ordinal ≥ N. Pods below the partition keep their original version even if deleted and recreated. This enables canary rollouts: set partition high, lower it incrementally as confidence grows.

**OnDelete**: no automatic rollout; Pods are only updated when you manually delete them.

## Deletion

- **Cascading delete** (default): deletes StatefulSet + all its Pods. PVCs remain.
- **Non-cascading delete**: `--cascade=orphan` — deletes only the StatefulSet object; Pods keep running unmanaged. Useful for StatefulSet version upgrades or migrations.

## Key Commands

```bash
# Prerequisites: two terminal windows (one for watching, one for commands)

# --- Create ---
kubectl apply -f https://k8s.io/examples/application/web/web.yaml
# Observe ordered Pod creation in watch terminal:
kubectl get pods --watch -l app=nginx

kubectl get service nginx          # headless service (ClusterIP: None)
kubectl get statefulset web

# --- Inspect identity ---
kubectl get pods -l app=nginx
for i in 0 1; do kubectl exec "web-$i" -- sh -c 'hostname'; done
# DNS lookup from a busybox Pod:
kubectl run -i --tty --image busybox:1.28 dns-test --restart=Never --rm
# Inside: nslookup web-0.nginx

# --- Stable storage ---
kubectl get pvc -l app=nginx
for i in 0 1; do kubectl exec "web-$i" -- sh -c 'echo "$(hostname)" > /usr/share/nginx/html/index.html'; done
for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
# Delete pods, verify data persists after recreation:
kubectl delete pod -l app=nginx
for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done

# --- Scaling ---
kubectl scale sts web --replicas=5
kubectl get pods --watch -l app=nginx
kubectl patch sts web -p '{"spec":{"replicas":3}}'
kubectl get pvc -l app=nginx   # 5 PVCs remain despite scale-down

# --- RollingUpdate ---
kubectl patch statefulset web --type='json' \
  -p='[{"op":"replace","path":"/spec/template/spec/containers/0/image","value":"registry.k8s.io/nginx-slim:0.24"}]'
kubectl get pod -l app=nginx --watch  # terminates in reverse order
for p in 0 1 2; do kubectl get pod "web-$p" --template '{{range $i,$c:=.spec.containers}}{{$c.image}}{{end}}'; echo; done

# --- Partitioned update (canary) ---
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":3}}}}'
kubectl patch statefulset web --type='json' \
  -p='[{"op":"replace","path":"/spec/template/spec/containers/0/image","value":"registry.k8s.io/nginx-slim:0.21"}]'
# Only pods with ordinal ≥ 3 update; others keep old image
# Lower partition to roll out further:
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":0}}}}'

# --- OnDelete strategy ---
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"OnDelete","rollingUpdate":null}}}'

# --- Non-cascading delete ---
kubectl delete statefulset web --cascade=orphan   # Pods keep running
kubectl get pods -l app=nginx                      # still there
kubectl apply -f https://k8s.io/examples/application/web/web.yaml  # recreate StatefulSet

# --- Cascading delete (default) ---
kubectl delete statefulset web    # Pods deleted too; PVCs survive
kubectl get pvc -l app=nginx      # PVCs still present — delete manually
kubectl delete pvc -l app=nginx
```

## Prerequisites

- A Kubernetes cluster with dynamic PV provisioning and a default StorageClass
- Two terminal windows (tutorial uses `--watch` extensively in parallel)
- Familiarity with Pods, Services, and PersistentVolumes

## Key Concepts

- **Headless Service** (`clusterIP: None`): required by StatefulSet for per-Pod DNS; does not load-balance
- **`volumeClaimTemplates`**: StatefulSet creates one PVC per Pod per template; PVCs named `<template-name>-<pod-name>`
- **PVCs are never auto-deleted**: not on Pod delete, not on scale-down, not on StatefulSet delete — must be deleted explicitly
- **Ordered creation/deletion**: guaranteed by the controller; new Pod waits for predecessor to be Running+Ready
- **Partition**: integer threshold in `spec.updateStrategy.rollingUpdate.partition`; only Pods with ordinal ≥ partition receive the new template; enables canary and phased rollouts
- **`kubectl rollout status sts/<name>`**: streams StatefulSet rollout progress (like `kubectl rollout status deployments`)
- **`--cascade=orphan`**: orphans Pods from the StatefulSet object without terminating them

## Cross-references

- [[cassandra]] — StatefulSet with custom seed provider and persistent storage for a real distributed database
- [[scale-app]] — `kubectl scale` mechanics (Deployment-focused, same syntax for StatefulSets)
- [[update-app]] — rolling update concepts (Deployment); compare with StatefulSet's partitioned rollout
- [[connect-applications-service]] — headless Service DNS and EndpointSlices
- [[kubernetes-topic-taxonomy]] — `statefulset`, `pvc`, `headless-service`, `partition`, `ordered` domains

## Sources

- `docs/wiki/raw/tutorials/basic-stateful-set.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/
