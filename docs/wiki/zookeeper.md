---
type: concept
title: Running ZooKeeper on Kubernetes
description: Production-grade StatefulSet deployment of a 3-node ZooKeeper ensemble — covering PodAntiAffinity to spread across nodes, PodDisruptionBudgets for planned maintenance, liveness probes, non-root security contexts, rolling updates, and cordon/drain resilience.
resource: https://kubernetes.io/docs/tutorials/stateful-application/zookeeper/
tags: [zookeeper, statefulset, poddisruptionbudget, podantiaffinity, pvc, liveness-probe, security-context, rolling-update, quorum]
timestamp: 2026-08-07T00:00:00Z
---

# Running ZooKeeper on Kubernetes

This is the most comprehensive stateful application tutorial in the Kubernetes docs. It deploys a 3-node Apache ZooKeeper ensemble and systematically exercises every production concern: topology spreading, failure handling, maintenance safety, liveness, logging, security, rolling updates, and node-level disruption. It builds directly on [[basic-stateful-set]] and [[cassandra]] but goes significantly further.

**ZooKeeper primer:** ZooKeeper uses the Zab consensus protocol — a quorum-based leader election and replicated state machine. A 3-node ensemble can tolerate 1 failure (majority quorum = 2 of 3). All writes are atomically replicated; reads can be served by any node. Data is stored in memory + WAL + periodic snapshots, all persisted to the PVC.

## Architecture: what the manifest deploys

```
zk-hs (headless Service, clusterIP: None) — per-Pod DNS for server-to-server communication
zk-cs (regular Service, port 2181)         — client access to the ensemble
zk-pdb (PodDisruptionBudget, maxUnavailable:1) — quorum protection during maintenance
zk   (StatefulSet, 3 replicas)             — zk-0, zk-1, zk-2 with 10Gi PVCs each
```

**PodAntiAffinity (required):** `requiredDuringSchedulingIgnoredDuringExecution` with `topologyKey: kubernetes.io/hostname` ensures each ZooKeeper Pod lands on a different node. Without this, two Pods on the same node means a single node failure loses quorum. This requires at least 3 worker nodes.

**Stable identity → consistent config:** Each Pod's ordinal (0, 1, 2) is used as ZooKeeper's `myid` (ordinal + 1 = 1, 2, 3). The `zoo.cfg` is generated with the stable FQDNs (`zk-0.zk-hs.default.svc.cluster.local:2888:3888`, etc.) so every server knows the full membership. This is the key insight: StatefulSet stable identity maps directly to ZooKeeper's explicit membership requirement.

**PodDisruptionBudget:** `maxUnavailable: 1` means `kubectl drain` will refuse to evict a second ZooKeeper Pod if one is already disrupted. This prevents losing quorum during rolling node maintenance. Without a PDB, an operator draining two nodes simultaneously would bring down the ensemble.

## Key Commands

```bash
# Deploy everything at once
kubectl apply -f https://k8s.io/examples/application/zookeeper/zookeeper.yaml

# Watch ordered Pod creation
kubectl get pods -w -l app=zk

# Verify stable hostnames and myid assignment
for i in 0 1 2; do kubectl exec zk-$i -- hostname; done
for i in 0 1 2; do echo "myid zk-$i"; kubectl exec zk-$i -- cat /var/lib/zookeeper/data/myid; done
for i in 0 1 2; do kubectl exec zk-$i -- hostname -f; done  # FQDNs

# Inspect zoo.cfg (server list uses FQDNs)
kubectl exec zk-0 -- cat /opt/zookeeper/conf/zoo.cfg

# Sanity test: write to zk-0, read from zk-1 (proves replication)
kubectl exec zk-0 -- zkCli.sh create /hello world
kubectl exec zk-1 -- zkCli.sh get /hello

# Durability: delete StatefulSet, reapply, verify data survives
kubectl delete statefulset zk
kubectl get pods -w -l app=zk
kubectl apply -f https://k8s.io/examples/application/zookeeper/zookeeper.yaml
kubectl exec zk-2 zkCli.sh get /hello   # still returns "world"

# Verify PVCs persist through StatefulSet deletion
kubectl get pvc -l app=zk   # datadir-zk-0, datadir-zk-1, datadir-zk-2 still Bound

# Verify non-root execution
kubectl exec zk-0 -- ps -elf   # process runs as zookeeper user (UID 1000)

# Liveness probe: deleting the health script triggers restart
kubectl exec zk-0 -- rm /opt/zookeeper/bin/zookeeper-ready
kubectl get pod -w -l app=zk   # zk-0 restarts after probe fails

# Process failure: kill ZooKeeper JVM, kubelet restarts container
kubectl exec zk-0 -- pkill java
kubectl get pod -w -l app=zk   # zk-0 shows Error → Running (RESTARTS: 1)

# Rolling update (e.g., change CPU request)
kubectl patch sts zk --type='json' \
  -p='[{"op":"replace","path":"/spec/template/spec/containers/0/resources/requests/cpu","value":"0.3"}]'
kubectl rollout status sts/zk
kubectl rollout history sts/zk
kubectl rollout undo sts/zk

# Node failure simulation: cordon a node
kubectl get pod -o wide -l app=zk   # note which node each pod is on
kubectl cordon <node-name>
kubectl drain <node-name> --ignore-daemonsets --force --delete-emptydir-data
# PDB prevents draining if another ZK pod is already disrupted

# Cleanup (PVCs must be deleted manually)
kubectl delete -f https://k8s.io/examples/application/zookeeper/zookeeper.yaml
kubectl delete pvc -l app=zk
```

## Prerequisites

- At least 4 worker nodes (3 for ZooKeeper Pods + 1 for cordon/drain testing), each with 2 CPUs and 4 GiB RAM
- Dynamic PV provisioning (or 3 manually-provisioned 20 GiB volumes)
- Dedicated cluster recommended — the tutorial cordons and drains nodes, evicting all workloads from them
- Strong familiarity with StatefulSets and PVCs ([[basic-stateful-set]])

## Key Concepts

- **`requiredDuringSchedulingIgnoredDuringExecution` PodAntiAffinity**: hard scheduling constraint — Pod is unschedulable if no node satisfies the rule; unlike `preferred`, this is never violated; essential for quorum-sensitive applications
- **PodDisruptionBudget `maxUnavailable: 1`**: limits voluntary disruptions (drain, eviction); `kubectl drain` blocks if eviction would violate the PDB; prevents quorum loss during planned maintenance
- **`myid` file + ordinal mapping**: ZooKeeper requires a unique integer identity; StatefulSet ordinal + 1 provides this deterministically and stably across restarts
- **WAL + snapshot durability**: ZooKeeper writes commits to a WAL before acknowledging them; periodic snapshots allow fast recovery; both live in the PVC → data survives Pod deletion
- **`ruok`/`imok` four-letter word**: ZooKeeper's built-in health check protocol; the liveness probe script sends `ruok` to port 2181 and expects `imok` back
- **`securityContext.runAsUser + fsGroup`**: ensures ZooKeeper runs as UID 1000 (zookeeper user) with the PVC owned by GID 1000 (zookeeper group) — non-root principle
- **Logging to stdout**: ZooKeeper's Log4j config routes all logs to the console; kubelet captures stdout/stderr for `kubectl logs`; avoids filling the PVC with log files
- **PDB + PodAntiAffinity together**: the combination is the production safety net — anti-affinity spreads Pods; PDB limits how many can be disrupted at once; quorum is preserved through both node failures and maintenance

## Cross-references

- [[basic-stateful-set]] — foundational StatefulSet concepts this tutorial builds on (stable identity, PVC lifecycle, ordered ops, rolling updates)
- [[cassandra]] — similar pattern: distributed system + StatefulSet + headless Service + PVC; less focus on resilience primitives
- [[pods-and-endpoint-termination-flow]] — graceful termination during rolling updates affects ZooKeeper quorum windows
- [[connect-applications-service]] — headless Service DNS mechanics underpinning ZooKeeper's stable FQDNs
- [[kubernetes-topic-taxonomy]] — `statefulset`, `poddisruptionbudget`, `podantiaffinity`, `quorum` domains

## Sources

- `docs/wiki/raw/tutorials/zookeeper.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/stateful-application/zookeeper/
