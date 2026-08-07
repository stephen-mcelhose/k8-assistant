---
type: concept
title: Exposing an External IP Address
description: How to expose a multi-replica Deployment to the internet using a LoadBalancer Service backed by a cloud provider, and how to verify endpoints and clean up.
resource: https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/
tags: [service, loadbalancer, external-ip, expose, deployment, cloud, basics]
timestamp: 2026-08-07T00:00:00Z
---

# Exposing an External IP Address

This tutorial shows how to give a Deployment a publicly routable IP address using a `LoadBalancer`-type Service. Unlike [[expose-app]] (which uses `NodePort` on minikube), this approach requires a cloud provider — GKE, EKS, AKS, or similar — that can provision a real cloud load balancer on demand. The tutorial is intentionally short: it is concerned with the mechanics of `kubectl expose` and `kubectl describe services`, not with application logic.

The workload is a five-replica `hello-world` Deployment deployed directly from a remote manifest with `kubectl apply -f <URL>`. Once running, a single `kubectl expose` command creates the LoadBalancer Service. The external IP initially shows as `<pending>` while the cloud provider allocates and provisions the load balancer — this is expected and usually resolves within a minute. `kubectl describe services` then reveals the full topology: ClusterIP (cluster-internal stable IP), LoadBalancer Ingress (the external IP), Port (service port), NodePort (the node-level port the LB forwards to), and Endpoints (the individual Pod IPs backing the service).

The tutorial closes with an explicit cleanup sequence — `kubectl delete services` followed by `kubectl delete deployment` — which is a good habit to internalise: Services and Deployments are independent objects and must be deleted separately.

**Relationship to other Service types:** `LoadBalancer` is the production-grade mechanism for external access on cloud infrastructure. `NodePort` ([[expose-app]]) is the minikube-friendly alternative. `ClusterIP` (default) is cluster-internal only. Ingress controllers sit above all three and are out of scope here.

## Key Commands

```bash
# Deploy from a remote manifest
kubectl apply -f https://k8s.io/examples/service/load-balancer-example.yaml

# Inspect the Deployment and its ReplicaSet
kubectl get deployments hello-world
kubectl describe deployments hello-world
kubectl get replicasets
kubectl describe replicasets

# Create a LoadBalancer Service
kubectl expose deployment hello-world --type=LoadBalancer --name=my-service

# Check for external IP (repeat until no longer <pending>)
kubectl get services my-service

# Full service detail: ClusterIP, Ingress, Port, NodePort, Endpoints
kubectl describe services my-service

# Verify endpoint IPs match pod IPs
kubectl get pods --output=wide

# Access the application
curl http://<external-ip>:8080

# minikube alternative (opens browser)
minikube service my-service

# Cleanup
kubectl delete services my-service
kubectl delete deployment hello-world
```

## Prerequisites

- A cloud-provider Kubernetes cluster (GKE, EKS, AKS, etc.) — **not** plain minikube, which has no LoadBalancer provisioner by default
- `kubectl` configured to reach the cluster's API server
- Understanding of Deployments and ReplicaSets ([[deploy-app]], [[scale-app]])

## Key Concepts

- **LoadBalancer Service**: provisions a cloud load balancer with a stable external IP; the LB forwards to NodePort, which forwards to Pod endpoints
- **`<pending>` external IP**: normal while the cloud provider allocates the LB — check again after ~60 s
- **Endpoints**: the live Pod IPs backing a Service; shown in `kubectl describe services` and correlate to `kubectl get pods -o wide`
- **Port vs NodePort**: `Port` is the service-level port clients use; `NodePort` is the node-level port the LB routes to internally

## Cross-references

- [[expose-app]] — NodePort equivalent for minikube; compare Service types
- [[deploy-app]] — creates the Deployment this tutorial builds on conceptually
- [[scale-app]] — explains ReplicaSets referenced in Deployment describe output
- [[connect-applications-service]] — deep dive into Service DNS, ClusterIP, and multi-port configuration
- [[kubernetes-topic-taxonomy]] — `service`, `loadbalancer`, `external-ip` domains

## Sources

- `docs/wiki/raw/tutorials/expose-external-ip.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/
