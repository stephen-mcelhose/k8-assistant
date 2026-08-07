---
type: concept
title: Deploy an App (Using kubectl to Create a Deployment)
description: How to deploy a containerised application to Kubernetes using kubectl create deployment, and how to access it through the kubectl proxy before a Service exists.
resource: https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/
tags: [deployment, kubectl, create-deployment, proxy, pod, node, replica, self-healing, basics]
timestamp: 2026-08-07T15:50:27Z
---

# Deploy an App (Using kubectl to Create a Deployment)

This tutorial is the first hands-on step of the Kubernetes Basics series. It introduces the **Deployment** as the canonical abstraction for running application instances on Kubernetes. A Deployment tells the control plane what container image to run and how many replicas to maintain; the Deployment controller then handles scheduling onto Nodes and automatically reschedules instances when a Node fails. This self-healing behaviour is the key difference from pre-orchestration approaches (scripts that start apps but cannot recover from machine failure).

The tutorial uses a minimal "hello-world" image (`gcr.io/google-samples/kubernetes-bootcamp:v1`) to keep the focus on the Deployment lifecycle rather than the application itself. It requires AMD64 architecture and a POSIX shell (bash/zsh); Windows users need WSL or Git Bash. A running cluster with `kubectl` configured is the only other prerequisite — the tutorial assumes minikube or equivalent, but any cluster works.

After creating the Deployment with a single command, the tutorial explains why Pods are not immediately reachable from outside the cluster: they live on a **private, isolated network**. The workaround before a Service exists is `kubectl proxy`, which opens a local tunnel to the Kubernetes API server. Through that tunnel, the API server exposes a per-Pod endpoint at `/api/v1/namespaces/default/pods/<POD_NAME>:8080/proxy/`, making it possible to curl the running app directly. This proxy approach is a teaching scaffold — production access uses Services and Ingress (see [[expose-app]]).

See [[tutorial-coverage-scoring]] for why this tutorial scores 4.0 — the highest context score in the 26-tutorial set — making it the recommended starting point for all learners.

## Key Commands

```bash
# Verify kubectl can reach the cluster
kubectl version

# List available nodes
kubectl get nodes

# Create a Deployment (image + name required)
kubectl create deployment kubernetes-bootcamp \
  --image=gcr.io/google-samples/kubernetes-bootcamp:v1

# List deployments to confirm it started
kubectl get deployments

# Open a proxy to the cluster's private network (separate terminal)
kubectl proxy

# Inspect cluster version through the proxy
curl http://localhost:8001/version

# Capture the Pod name for direct API access
export POD_NAME=$(kubectl get pods \
  -o go-template --template '{{range .items}}{{.metadata.name}}{{"\\n"}}{{end}}')

# Reach the running Pod via the API proxy
curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME:8080/proxy/
```

## Prerequisites

- `kubectl` installed and configured to reach a running cluster
- AMD64 CPU (or minikube with Docker Desktop driver for emulation)
- POSIX shell (bash / zsh / sh); Windows → WSL or Git Bash

## Cross-references

- [[explore-app]] — inspects the Pods created by this Deployment using describe/logs/exec (Tutorial #3)
- [[expose-app]] — adds a Service so the Deployment is reachable without the proxy (Tutorial #4)
- [[scale-app]] — scales the replica count of this Deployment; introduces ReplicaSets and load balancing (Tutorial #5)
- [[tutorial-coverage-scoring]] — explains the 4.0 score and sequencing rationale
- [[kubernetes-topic-taxonomy]] — canonical tag vocabulary; `deployment` and `proxy` domains

## Sources

- `docs/wiki/raw/tutorials/deploy-app.md`
- https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/
