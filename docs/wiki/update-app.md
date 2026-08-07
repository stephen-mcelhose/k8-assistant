---
type: concept
title: Performing a Rolling Update
description: How Kubernetes rolling updates replace Pods incrementally with zero downtime, how to trigger an update with kubectl set image, verify with rollout status, and roll back with rollout undo.
resource: https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/
tags: [rollout, rollback, rolling-update, set-image, image, deployment, zero-downtime, basics]
timestamp: 2026-08-07T00:00:00Z
---

# Performing a Rolling Update

Rolling updates let you change a Deployment's container image (or other Pod template fields) with **zero downtime**. Kubernetes replaces old Pods incrementally: it creates a new Pod, waits for it to become ready, then removes an old one — repeating until all replicas run the new version. By default, at most 1 Pod may be unavailable and at most 1 new Pod may be created above the desired count at any time (both configurable as numbers or percentages). The Service continues routing traffic only to healthy Pods throughout.

`kubectl set image` is the key command: it updates the container image in the Deployment spec and triggers the rollout. `kubectl rollout status` streams progress. `kubectl describe pods` shows the `Image:` field, confirming which version is running.

The tutorial also covers **rollback**: when a bad image tag (e.g., `v10` that doesn't exist in the registry) causes `ImagePullBackOff`, `kubectl rollout undo` reverts to the last known-good state. Updates are versioned — you can roll back to any previous revision, not just the most recent. After undo, `kubectl describe pods` confirms the image reverted to `v2`.

A practical implication: because rolling updates require multiple Pods to work correctly (one down while another comes up), **scaling to more than 1 replica is a prerequisite for zero-downtime updates**. That's why [[scale-app]] precedes this tutorial in the Basics series.

## Key Commands

```bash
# Confirm current state
kubectl get deployments
kubectl get pods
kubectl describe pods   # look for Image: field

# Trigger a rolling update to a new image version
kubectl set image deployments/kubernetes-bootcamp \
  kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v2

# Watch Pod replacement in progress
kubectl get pods

# Verify rollout completed successfully
kubectl rollout status deployments/kubernetes-bootcamp
kubectl describe pods   # Image: should show v2

# Restore Service if deleted in previous tutorial
kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080
export NODE_PORT="$(kubectl get services/kubernetes-bootcamp \
  -o go-template='{{(index .spec.ports 0).nodePort}}')"
curl http://"$(minikube ip):$NODE_PORT"   # all Pods return v2

# Simulate a bad update (image does not exist)
kubectl set image deployments/kubernetes-bootcamp \
  kubernetes-bootcamp=gcr.io/google-samples/kubernetes-bootcamp:v10
kubectl get deployments    # desired count not reached
kubectl get pods           # some Pods show ImagePullBackOff
kubectl describe pods      # Events section shows pull failure

# Roll back to the previous working version
kubectl rollout undo deployments/kubernetes-bootcamp
kubectl get pods           # Pods replaced again
kubectl describe pods      # Image: reverted to v2

# Clean up
kubectl delete deployments/kubernetes-bootcamp services/kubernetes-bootcamp
```

## Prerequisites

- A scaled Deployment from [[scale-app]] (multiple replicas for zero-downtime)
- A Service from [[expose-app]] for traffic verification during update
- minikube or equivalent cluster

## Key Concepts

- **Rolling update**: incremental Pod replacement — new Pod ready before old Pod removed
- **Max unavailable / max surge**: both default to 1; configure in `strategy.rollingUpdate` in the Deployment spec
- **`kubectl set image`**: patches the container image in the Deployment's Pod template, triggering the rollout
- **`kubectl rollout status`**: streams rollout progress; exits 0 on success
- **`kubectl rollout undo`**: reverts to the previous Deployment revision
- **`ImagePullBackOff`**: the image could not be pulled — check the tag exists in the registry; use `kubectl describe pods` → Events for details
- **Versioned updates**: each Deployment change increments a revision counter; `kubectl rollout history` shows all revisions

## Cross-references

- [[scale-app]] — scaling to multiple replicas, a prerequisite for zero-downtime updates
- [[expose-app]] — the Service that keeps routing traffic during the update
- [[deploy-app]] — the Deployment object being updated
- [[kubernetes-topic-taxonomy]] — `rollout`, `rollback`, `rolling-update`, `set-image` domains

## Sources

- `docs/wiki/raw/tutorials/update-app.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/
