---
type: concept
title: Explore Your App (Viewing Pods and Nodes)
description: How to inspect running Pods and Nodes using kubectl describe, kubectl logs, and kubectl exec — the core debugging toolkit for any Kubernetes workload.
resource: https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/
tags: [pod, node, describe, logs, exec, proxy, debug, troubleshooting, kubelet, basics]
timestamp: 2026-08-07T15:54:49Z
---

# Explore Your App (Viewing Pods and Nodes)

This tutorial introduces the two foundational Kubernetes resource types below the Deployment level: **Pods** and **Nodes**. A Pod is the atomic unit of scheduling — a group of one or more tightly coupled containers sharing a single IP address, port space, and storage volumes. Pods are created by Deployments (see [[deploy-app]]), not by users directly; when a Deployment's replica count is 1, there is exactly one Pod per Deployment. Pods are co-located on a Node and rescheduled automatically to another Node if the original Node fails.

A **Node** is a worker machine (physical or virtual) managed by the control plane. Every Node runs two mandatory components: **kubelet** (the agent that communicates with the control plane and manages Pod lifecycle) and a **container runtime** (pulls images, unpacks, runs containers). The control plane's scheduler places Pods onto Nodes based on available resources; users do not assign Pods to Nodes directly in normal operation.

The tutorial's hands-on focus is **troubleshooting**. The four kubectl verbs introduced here — `get`, `describe`, `logs`, `exec` — form the core debugging toolkit for any Kubernetes workload. `kubectl describe pods` is particularly valuable: it surfaces the Pod's IP, its container images and ports, and a chronological event log covering scheduling, pulling, and starting. `kubectl exec` opens a shell or runs a one-shot command inside a running container, enabling direct inspection of the filesystem and environment. Note that `kubectl describe` output is intentionally human-readable and should not be parsed in scripts; use `-o json` or `-o jsonpath` for machine-readable output.

Because Pods live on a private cluster network, `kubectl proxy` is again required to reach them from outside the cluster (same approach as [[deploy-app]]). This remains a teaching scaffold — Tutorial #4 ([[expose-app]]) replaces the proxy with a proper Service.

## Key Commands

```bash
# List all pods in the current namespace
kubectl get pods

# Detailed info on all pods: IP, ports, container images, events
kubectl describe pods

# Describe a specific pod by name
kubectl describe pod <pod-name>

# Open proxy to private cluster network (separate terminal)
kubectl proxy

# Capture pod name into a variable
export POD_NAME="$(kubectl get pods \
  -o go-template --template '{{range .items}}{{.metadata.name}}{{"\\n"}}{{end}}')"

# Access Pod through proxy
curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME:8080/proxy/

# Print environment variables inside the container
kubectl exec "$POD_NAME" -- env

# Open an interactive shell inside the container
kubectl exec -ti $POD_NAME -- bash

# (inside container) view app source
cat server.js

# (inside container) curl the app on its loopback interface
curl http://localhost:8080
```

## Prerequisites

- A running Deployment from [[deploy-app]] (Tutorial #2)
- POSIX shell (bash / zsh / sh); Windows → WSL or Git Bash
- `kubectl proxy` running in a second terminal for proxy-based access

## Cross-references

- [[deploy-app]] — creates the Deployment and Pods this tutorial inspects (Tutorial #2)
- [[expose-app]] — replaces the proxy with a Service for persistent external access (Tutorial #4)
- [[scale-app]] — shows how replica count changes the number of Pods; use `get pods -o wide` to see them distributed across Nodes (Tutorial #5)
- [[kubernetes-topic-taxonomy]] — `pod`, `node`, `debug`, `troubleshooting`, `exec`, `logs` domains
- [[tutorial-coverage-scoring]] — this tutorial scores 4.0; ideal second step after Deploy an App

## Sources

- `docs/wiki/raw/tutorials/explore-app.md`
- https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/
