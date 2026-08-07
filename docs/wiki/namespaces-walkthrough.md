---
type: concept
title: Namespaces Walkthrough
description: How to use Kubernetes namespaces to partition a cluster into isolated scopes, create per-namespace contexts with kubectl config, and switch between them.
resource: https://kubernetes.io/docs/tutorials/cluster-management/namespaces-walkthrough/
tags: [namespace, context, use-context, kubectl-config, isolation, cluster-management]
timestamp: 2026-08-07T00:00:00Z
---

# Namespaces Walkthrough

Namespaces give different teams or environments a scoped view of the same cluster: names are unique within a namespace but not across namespaces, and authorization policies can be applied per-namespace. The `default` namespace is created automatically; this tutorial adds `development` and `production` namespaces to demonstrate that resources created in one are invisible to users operating in the other.

Namespaces are created from manifests (`kubectl create -f`) or imperatively (`kubectl create namespace <name>`). The tutorial uses YAML manifests that set a `name` label on each namespace, which is a common convention for namespace selectors. Once the namespaces exist, the interesting work is on the client side: `kubectl config set-context` creates a named kubeconfig context that pins a cluster, user, and namespace together, letting you switch namespace scope with `kubectl config use-context` rather than appending `--namespace` to every command.

The tutorial demonstrates isolation concretely: after switching to the `dev` context, a `snowflake` Deployment with 2 replicas is created; switching to `prod` shows an empty cluster — `kubectl get deployment` and `kubectl get pods` return nothing. The namespaces genuinely hide each other's resources from the user's perspective, which is the key lesson.

**Important caveat:** The tutorial's kubeconfig examples contain redacted credentials (passwords, tokens) from a real cluster. These are illustrative only — never commit real kubeconfig credentials to source control.

## Key Commands

```bash
# See existing namespaces
kubectl get namespaces
kubectl get namespaces --show-labels

# Create namespaces from manifests
kubectl create -f https://k8s.io/examples/admin/namespace-dev.yaml
kubectl create -f https://k8s.io/examples/admin/namespace-prod.yaml

# Inspect current kubeconfig context
kubectl config view
kubectl config current-context

# Create named contexts pinned to each namespace
kubectl config set-context dev \
  --namespace=development \
  --cluster=<cluster-name> \
  --user=<user-name>

kubectl config set-context prod \
  --namespace=production \
  --cluster=<cluster-name> \
  --user=<user-name>

# Switch active context
kubectl config use-context dev
kubectl config use-context prod

# Deploy into the current namespace (no --namespace flag needed)
kubectl apply -f https://k8s.io/examples/admin/snowflake-deployment.yaml
kubectl get deployment
kubectl get pods -l app=snowflake

# Verify isolation: switch to prod and confirm dev resources are invisible
kubectl config use-context prod
kubectl get deployment   # returns nothing
kubectl get pods         # returns nothing
```

## Prerequisites

- A Kubernetes cluster (minikube works; tutorial recommends at least 2 worker nodes)
- Basic understanding of Pods, Services, and Deployments ([[deploy-app]], [[explore-app]])
- `kubectl` configured against the cluster

## Key Concepts

- **Namespace**: a virtual cluster within a cluster — scopes Names, RBAC, and ResourceQuotas
- **`kubectl config set-context`**: creates a kubeconfig context binding cluster + user + namespace
- **`kubectl config use-context`**: switches the active context (affects all subsequent `kubectl` calls)
- **`~/.kube/config`**: the file where contexts are stored; edited by `kubectl config` commands
- **Isolation**: resources in namespace A are not visible to users operating in namespace B — `kubectl get` only returns resources in the current namespace by default

## Cross-references

- [[deploy-app]] — Deployments created within a namespace
- [[expose-app]] — Services are also namespace-scoped
- [[connect-applications-service]] — DNS service discovery is namespace-aware (CoreDNS)
- [[kubernetes-topic-taxonomy]] — `namespace`, `context`, `use-context` domains

## Sources

- `docs/wiki/raw/tutorials/namespaces-walkthrough.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/cluster-management/namespaces-walkthrough/
