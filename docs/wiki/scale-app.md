---
type: concept
title: Scale Up Your App (Running Multiple Instances)
description: How to manually scale a Kubernetes Deployment up and down using kubectl scale, what ReplicaSets are, and how Services automatically load-balance across multiple Pod replicas.
resource: https://kubernetes.io/docs/tutorials/kubernetes-basics/scale/scale-intro/
tags: [scale, replicaset, replicas, load-balancing, deployment, kubectl, autoscale, basics]
timestamp: 2026-08-07T16:02:11Z
---

# Scale Up Your App (Running Multiple Instances)

Scaling in Kubernetes means adjusting the **replica count** on a Deployment — the number of identical Pods running the same container image. `kubectl scale` is the imperative command; alternatively, the replica count can be changed declaratively by editing the Deployment manifest and applying it. Either approach updates the same underlying field (`spec.replicas`) and triggers the Deployment controller to reconcile toward the new desired state.

The mechanism that enforces the desired replica count at runtime is the **ReplicaSet**. A Deployment doesn't manage Pods directly — it manages a ReplicaSet, which in turn manages Pods. The ReplicaSet name is derived from the Deployment name plus a random suffix seeded from `pod-template-hash` (e.g., `kubernetes-bootcamp-644c5687f4`). Users rarely interact with ReplicaSets directly; `kubectl get rs` is useful for debugging but day-to-day scaling goes through the Deployment.

Once multiple replicas are running, a **Service** automatically distributes traffic across all of them. The Service's integrated load balancer uses **endpoints** to track which Pods are healthy and available; unhealthy Pods are removed from the endpoint list so traffic is never sent to them. This load balancing is transparent — the Service IP and port stay constant regardless of how many Pods are behind it. This is also what makes rolling updates (see [[update-app]]) downtime-free: the old Pods handle traffic while new ones start up.

Scaling to zero (`--replicas=0`) is valid and terminates all Pods while leaving the Deployment object intact. Kubernetes also supports automatic scaling via the HorizontalPodAutoscaler (HPA), which adjusts replica count based on CPU/memory metrics, but that is outside the scope of this tutorial.

## Key Commands

```bash
# Inspect current Deployment state (READY, UP-TO-DATE, AVAILABLE columns)
kubectl get deployments

# View the ReplicaSet managed by the Deployment
kubectl get rs

# Scale up to 4 replicas
kubectl scale deployments/kubernetes-bootcamp --replicas=4

# Confirm new Pods are running (shows Node assignment and IP per Pod)
kubectl get pods -o wide

# Inspect Deployment events to confirm the scale action was recorded
kubectl describe deployments/kubernetes-bootcamp

# Find the NodePort the Service is exposed on
kubectl describe services/kubernetes-bootcamp

# Capture NodePort into a variable for curling
export NODE_PORT="$(kubectl get services/kubernetes-bootcamp \
  -o go-template='{{(index .spec.ports 0).nodePort}}')"

# Hit the app repeatedly — different Pod names in each response confirms load balancing
curl http://$(minikube ip):$NODE_PORT

# Scale back down to 2 replicas
kubectl scale deployments/kubernetes-bootcamp --replicas=2

# Confirm 2 Pods remain, 2 terminated
kubectl get pods -o wide
```

## Prerequisites

- A running Deployment from [[deploy-app]] (Tutorial #2)
- A Service of type `LoadBalancer` exposing the Deployment — from [[expose-app]] (Tutorial #4); if absent, create with:
  ```bash
  kubectl expose deployment/kubernetes-bootcamp --type="LoadBalancer" --port 8080
  ```
- POSIX shell (bash / zsh / sh); Windows → WSL or Git Bash
- Docker Desktop on macOS: run `minikube tunnel` or use `minikube service kubernetes-bootcamp --url` to reach NodePort services

## Cross-references

- [[deploy-app]] — creates the Deployment being scaled (Tutorial #2)
- [[explore-app]] — use `kubectl get pods -o wide` to verify replicas across Nodes (Tutorial #3)
- [[expose-app]] — the Service that load-balances across replicas (Tutorial #4)
- [[update-app]] — rolling updates are only safe/downtime-free when multiple replicas exist (Tutorial #6)
- [[kubernetes-topic-taxonomy]] — `scale`, `replicaset`, `replicas`, `load-balancing`, `autoscale` domains
- [[tutorial-coverage-scoring]] — scores 4.0; completes the Batch 1 basics trilogy with [[deploy-app]] and [[explore-app]]

## Sources

- `docs/wiki/raw/tutorials/scale-app.md`
- https://kubernetes.io/docs/tutorials/kubernetes-basics/scale/scale-intro/
