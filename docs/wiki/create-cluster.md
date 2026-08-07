---
type: concept
title: Create a Kubernetes Cluster with Minikube
description: Introduction to the Kubernetes cluster model — control plane vs worker nodes, the kubelet, and how to create a local single-node cluster with minikube start.
resource: https://kubernetes.io/docs/tutorials/kubernetes-basics/create-cluster/cluster-intro/
tags: [cluster, minikube, control-plane, node, kubelet, basics]
timestamp: 2026-08-07T00:00:00Z
---

# Create a Kubernetes Cluster with Minikube

This is Tutorial #1 in the Kubernetes Basics series — a brief conceptual introduction to the cluster model before any hands-on work. It explains the two resource types in every Kubernetes cluster and how to create a local development cluster with minikube.

## Cluster architecture

A Kubernetes cluster has two resource types:

- **Control Plane**: the cluster's management layer — schedules applications, maintains desired state, scales workloads, and rolls out updates. Runs API server, scheduler, controller manager, and etcd. In production, control plane components run on dedicated nodes.
- **Node** (worker): a VM or physical machine that runs application containers. Each node runs a **kubelet** — an agent that registers the node with the control plane and manages containers on it — plus a container runtime (containerd, CRI-O, or similar).

The **Kubernetes API** is the communication channel between all components and between end users and the cluster. kubectl is a client for the API.

**Minikube** creates a single-node local cluster (control plane and one worker on the same VM/process). It is a development and learning tool only — not for production. The minikube CLI provides `start`, `stop`, `status`, and `delete` commands.

## Key Commands

```bash
# Start a local cluster
minikube start

# Verify the cluster is running
minikube status

# Confirm kubectl can reach the cluster
kubectl cluster-info
kubectl get nodes
```

## Prerequisites

- minikube installed (see [minikube start](https://minikube.sigs.k8s.io/docs/start/))
- kubectl installed

## Key Concepts

- **Control Plane**: orchestrates the cluster — scheduling, scaling, self-healing, rolling updates; runs API server, scheduler, controller manager, etcd
- **Node**: executes workloads; kubelet on each node reports to the control plane via the Kubernetes API
- **Kubelet**: the node-level agent; ensures containers described in PodSpecs are running and healthy
- **Container runtime**: the low-level engine that runs containers (containerd, CRI-O); separate from kubelet
- **minikube**: single-node local cluster for development; not suitable for production

## Cross-references

- [[deploy-app]] — the next step: deploying your first application onto the cluster
- [[explore-app]] — inspecting Pods and Nodes after deployment
- [[namespaces-walkthrough]] — cluster partitioning after the cluster is running
- [[kubernetes-topic-taxonomy]] — `cluster`, `minikube`, `control-plane`, `node` domains

## Sources

- `docs/wiki/raw/tutorials/create-cluster.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/kubernetes-basics/create-cluster/cluster-intro/
