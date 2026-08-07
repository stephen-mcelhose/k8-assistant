---
type: concept
title: Deploying Cassandra with a StatefulSet
description: How to deploy a 3-node Apache Cassandra ring on Kubernetes using a StatefulSet with a headless Service, custom seed provider for Pod discovery, PersistentVolumeClaims per node, and nodetool for ring validation.
resource: https://kubernetes.io/docs/tutorials/stateful-application/cassandra/
tags: [cassandra, statefulset, headless-service, pvc, seed-provider, nodetool, storage, distributed]
timestamp: 2026-08-07T00:00:00Z
---

# Deploying Cassandra with a StatefulSet

This tutorial applies StatefulSet concepts from [[basic-stateful-set]] to a real distributed database. Cassandra requires persistent storage for data durability and a discovery mechanism for nodes to join a ring — both of which StatefulSets handle naturally. The tutorial deploys a 3-node Cassandra ring and demonstrates validation, scaling, and cleanup.

**Custom seed provider:** Standard Cassandra uses a static seed list. This tutorial uses a custom Kubernetes-aware seed provider that queries the Kubernetes API to discover new Cassandra Pods as they appear. The seed is bootstrapped via the env var `CASSANDRA_SEEDS=cassandra-0.cassandra.default.svc.cluster.local` — the stable DNS name of the first Pod via the headless Service. As new Pods start, the seed provider discovers them dynamically.

**Headless Service:** `clusterIP: None` gives each Cassandra Pod a stable DNS name (`cassandra-0.cassandra.default.svc.cluster.local`, etc.) without a load-balanced VIP. Clients and the seed provider resolve individual node addresses directly. This is the standard pattern for any peer-to-peer or ring-topology distributed system on Kubernetes.

**Storage:** Each Pod gets its own 1 GiB PVC via `volumeClaimTemplates` (mounted at `/cassandra_data`). PVCs survive Pod deletion and are remounted when the Pod restarts — Cassandra data persists through node failures and restarts. **Cleanup must explicitly delete PVCs** — the StatefulSet controller never auto-deletes them.

**Minikube resource note:** Cassandra is memory-hungry. The default minikube configuration (2048 MB) causes insufficient resource errors. Start minikube with `--memory 5120 --cpus=4`.

## Key Commands

```bash
# Minikube: increase resources first
minikube start --memory 5120 --cpus=4

# --- Deploy headless Service ---
kubectl apply -f https://k8s.io/examples/application/cassandra/cassandra-service.yaml
kubectl get svc cassandra    # CLUSTER-IP should be None

# --- Deploy 3-node StatefulSet ---
kubectl apply -f https://k8s.io/examples/application/cassandra/cassandra-statefulset.yaml
# Or if you need to modify for your cluster:
# kubectl apply -f cassandra-statefulset.yaml

# Watch ordered Pod creation (can take several minutes per Pod)
kubectl get statefulset cassandra
kubectl get pods -l="app=cassandra"

# --- Validate ring ---
kubectl exec -it cassandra-0 -- nodetool status
# Shows Status/State for each node: UN = Up/Normal (healthy)

# --- Scale up ---
kubectl edit statefulset cassandra   # change replicas: 3 → 4
kubectl get statefulset cassandra    # verify DESIRED and CURRENT match

# --- Cleanup (must delete PVCs explicitly) ---
grace=$(kubectl get pod cassandra-0 -o=jsonpath='{.spec.terminationGracePeriodSeconds}') \
  && kubectl delete statefulset -l app=cassandra \
  && echo "Sleeping ${grace} seconds" 1>&2 \
  && sleep $grace \
  && kubectl delete persistentvolumeclaim -l app=cassandra
kubectl delete service -l app=cassandra
```

## Prerequisites

- A Kubernetes cluster with dynamic PV provisioning and a StorageClass named `fast` (or edit the manifest)
- For minikube: `minikube start --memory 5120 --cpus=4`
- Understanding of StatefulSets and PVCs ([[basic-stateful-set]])
- Kubernetes v1.14+ (`apps/v1` StatefulSet API)

## Key Concepts

- **Cassandra ring**: a peer-to-peer distributed database with no single leader; all nodes are equal
- **Seed provider**: the mechanism Cassandra uses to bootstrap ring discovery; the custom provider queries Kubernetes API instead of using a static IP list
- **`nodetool status`**: Cassandra's ring health check — `UN` (Up/Normal) means the node is healthy and participating
- **`terminationGracePeriodSeconds: 500`**: Cassandra needs a long grace period to flush data to disk (`nodetool drain` runs in `lifecycle.preStop`)
- **`kubectl edit statefulset`**: in-place edit to scale or modify the StatefulSet; triggers a rolling update
- **PVC cleanup required**: unlike Pods, PVCs are never auto-deleted — always `kubectl delete persistentvolumeclaim -l app=cassandra` after deleting the StatefulSet
- **StorageClass `fast`**: the manifest includes a `StorageClass` definition for minikube; for cloud clusters, update the `storageClassName` field

## Cross-references

- [[basic-stateful-set]] — foundational StatefulSet concepts: ordered operations, stable identity, PVC lifecycle, update strategies
- [[connect-applications-service]] — headless Service DNS mechanics
- [[kubernetes-topic-taxonomy]] — `statefulset`, `pvc`, `headless-service`, `distributed` domains

## Sources

- `docs/wiki/raw/tutorials/cassandra.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/stateful-application/cassandra/
