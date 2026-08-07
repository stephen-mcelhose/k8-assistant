---
type: concept
title: Tutorial Sync Plan
description: Plan for fetching and ingesting all 26 official kubernetes.io tutorials into the wiki as raw sources, plus a maintenance strategy for keeping them current.
tags: [tutorials, sync, maintenance, ingestion, plan]
timestamp: 2026-08-07T15:39:38Z
---

# Tutorial Sync Plan

The `references/tutorial-map.md` maps 26 official kubernetes.io tutorials by score and tags (see [[tutorial-coverage-scoring]]). The next step is to fetch each tutorial's full content and ingest it into the wiki, so the skill has synthesized, cross-linked knowledge rather than just a scoring table.

## Target tutorials

Ordered by Context Score (highest first — best return on first ingest):

| # | Tutorial | URL | Context Score | Tags (sample) |
|---|----------|-----|---------------|---------------|
| 2 | Deploy an App | https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/ | 4.0 | deployment, apply, get |
| 3 | Explore Your App | https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/ | 4.0 | pod, describe, logs, debug |
| 5 | Scale Up Your App | https://kubernetes.io/docs/tutorials/kubernetes-basics/scale/scale-intro/ | 4.0 | scale, replicaset, autoscale |
| 14 | Exposing External IP Address | https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/ | 3.2 | loadbalancer, external-ip |
| 23 | Namespaces Walkthrough | https://kubernetes.io/docs/tutorials/cluster-management/namespaces-walkthrough/ | 3.2 | namespace, context, use-context |
| 4 | Expose Your App Publicly | https://kubernetes.io/docs/tutorials/kubernetes-basics/expose/expose-intro/ | 3.0 | service, nodeport, selector |
| 6 | Update Your App | https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/ | 3.0 | rollout, rollback, image |
| 8 | Configuring Redis using ConfigMap | https://kubernetes.io/docs/tutorials/configuration/configure-redis-using-configmap/ | 3.0 | configmap, volume, exec |
| 15 | Deploying PHP Guestbook with Redis | https://kubernetes.io/docs/tutorials/stateless-application/guestbook/ | 3.0 | guestbook, port-forward |
| 24 | Connecting Applications with Services | https://kubernetes.io/docs/tutorials/services/connect-applications-service/ | 3.0 | service, dns, coredns, tls |
| 11 | Pod Security Standards (Namespace) | https://kubernetes.io/docs/tutorials/security/ns-level-pss/ | 2.4 | pod-security, namespace |
| 7 | Updating Configuration via ConfigMap | https://kubernetes.io/docs/tutorials/configuration/updating-configuration-via-a-configmap/ | 2.0 | configmap, rollout, environment |
| 9 | Adopting Sidecar Containers | https://kubernetes.io/docs/tutorials/configuration/pod-sidecar-containers/ | 2.0 | sidecar, init-containers |
| 16 | StatefulSet Basics | https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/ | 2.0 | statefulset, pvc, rolling-update |
| 18 | Deploying Cassandra with StatefulSet | https://kubernetes.io/docs/tutorials/stateful-application/cassandra/ | 2.0 | cassandra, statefulset |
| 1 | Create a Kubernetes Cluster | https://kubernetes.io/docs/tutorials/kubernetes-basics/create-cluster/cluster-intro/ | 1.9 | cluster, minikube |
| 17 | WordPress and MySQL with Persistent Volumes | https://kubernetes.io/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/ | 1.9 | wordpress, mysql, kustomize |
| 26 | Explore Termination Behavior | https://kubernetes.io/docs/tutorials/services/pods-and-endpoint-termination-flow/ | 1.9 | termination, graceful-shutdown |
| 25 | Using Source IP | https://kubernetes.io/docs/tutorials/services/source-ip/ | 1.6 | source-ip, nat, kube-proxy |
| 12 | Restrict Container Access with AppArmor | https://kubernetes.io/docs/tutorials/security/apparmor/ | 1.2 | apparmor, security-context |
| 13 | Restrict Container Syscalls with seccomp | https://kubernetes.io/docs/tutorials/security/seccomp/ | 1.2 | seccomp, syscall |
| 21 | Configuring Swap Memory | https://kubernetes.io/docs/tutorials/cluster-management/provision-swap-memory/ | 1.2 | swap, kubelet |
| 19 | Running ZooKeeper | https://kubernetes.io/docs/tutorials/stateful-application/zookeeper/ | 1.0 | zookeeper, poddisruptionbudget |
| 10 | Pod Security Standards (Cluster) | https://kubernetes.io/docs/tutorials/security/cluster-level-pss/ | 0.8 | pod-security, kind, admission-controller |
| 20 | Running Kubelet in Standalone Mode | https://kubernetes.io/docs/tutorials/cluster-management/kubelet-standalone/ | 0.8 | kubelet, cri-o, cni |
| 22 | Install Drivers and Allocate Devices with DRA | https://kubernetes.io/docs/tutorials/cluster-management/install-use-dra/ | 0.8 | dra, deviceclass, cel |

## Ingest process (per tutorial)

For each tutorial, the llm-wiki ingest operation should:

1. `WebFetch` the tutorial URL
2. Write the raw content to `docs/wiki/raw/tutorials/<slug>.md` (immutable after write)
3. Create a wiki page at `docs/wiki/<slug>.md` with:
   - OKF frontmatter (`type: concept`, `title`, `description`, `resource`, `tags`, `timestamp`)
   - 2–4 paragraph synthesis (what the tutorial teaches, what environment it assumes, what commands it exercises)
   - **Key Commands** section — the kubectl commands exercised
   - **Prerequisites** section — what the learner needs before starting
   - **Cross-references** — `[[wikilinks]]` to related taxonomy entries and other tutorials
   - `## Sources` at the bottom
4. Propagate: update any existing wiki pages that reference this tutorial's topics
5. Update `index.md` and append to `log.md`

## Batching recommendation

Run in score-descending order (highest first) so the most useful pages are available earliest. Suggested batches:

| Batch | Tutorials | Score range | Notes |
|-------|-----------|-------------|-------|
| 1 | #2, 3, 5 | 4.0 | Kubernetes basics — highest value, most beginner traffic |
| 2 | #14, 23, 4, 6, 8, 15, 24 | 3.0–3.2 | Services, networking, rolling updates |
| 3 | #11, 7, 9, 16, 18 | 2.0–2.4 | Configuration, stateful apps |
| 4 | #1, 17, 26, 25 | 1.9 | Cluster setup, termination, source IP |
| 5 | #12, 13, 21, 19 | 1.0–1.2 | Advanced security, swap, ZooKeeper |
| 6 | #10, 20, 22 | 0.8 | Cluster-level security, kubelet, DRA |

## Maintenance / sync strategy

kubernetes.io tutorials are versioned with Kubernetes releases. To keep the wiki current:

1. **Quarterly check**: re-fetch each raw tutorial URL and diff against the stored raw file. If content changed, re-ingest (update the wiki page, preserve the old raw as `<slug>-<date>.md`).
2. **New tutorial detection**: monitor the kubernetes.io tutorials index page for new entries. Add to `tutorial-map.md` and ingest.
3. **Score recalibration**: if `quick-reference.md` is updated (new commands added), recalculate context scores for affected tutorials.

The `log.md` append-only log provides a natural audit trail for when each tutorial was last fetched.

## Sources

- `references/tutorial-map.md` — full 26-tutorial table with scores and tags
- `docs/pr-notes.md` — original PR analysis establishing the tutorial set
