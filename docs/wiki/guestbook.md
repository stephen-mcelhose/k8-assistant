---
type: concept
title: PHP Guestbook with Redis (Multi-Tier App)
description: How to deploy a multi-tier stateless application on Kubernetes — Redis leader/follower backend plus a PHP frontend — using Services for inter-tier DNS discovery and port-forward for local access.
resource: https://kubernetes.io/docs/tutorials/stateless-application/guestbook/
tags: [guestbook, port-forward, redis, multi-tier, service, deployment, scale, labels, dns]
timestamp: 2026-08-07T00:00:00Z
---

# PHP Guestbook with Redis (Multi-Tier App)

This tutorial assembles the building blocks from earlier tutorials into a real multi-tier application: a Redis leader (1 replica) for writes, Redis followers (2 replicas) for reads, and a PHP frontend (3 replicas) serving the UI. It demonstrates how Services enable tier-to-tier communication via DNS, how `kubectl port-forward` gives local access without a cloud load balancer, and how scaling and cleanup work at the application level.

Each tier follows the same pattern: a **Deployment** (manages Pod replicas) + a **Service** (provides a stable DNS name for other tiers to discover it). The frontend Pod is configured with `GET_HOSTS_FROM=dns`, meaning it resolves `redis-leader` and `redis-follower` by DNS name rather than hardcoded IPs — this is how ClusterIP Services work: CoreDNS assigns `<service-name>.<namespace>.svc.cluster.local`, resolvable by any Pod in the cluster.

The frontend Service defaults to **ClusterIP** (cluster-internal only). For local access without a cloud LB, `kubectl port-forward svc/frontend 8080:80` tunnels traffic from `localhost:8080` to the Service. The manifest also shows how to optionally switch to `LoadBalancer` type — uncomment `type: LoadBalancer` in the YAML.

**Scaling** works the same as [[scale-app]]: `kubectl scale deployment frontend --replicas=5` adds Pods; the Service automatically routes to all of them. Cleanup uses label selectors to delete multiple resources in one command, which is cleaner than listing each resource individually.

## Key Commands

```bash
# --- Redis leader ---
kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-deployment.yaml
kubectl get pods
kubectl logs -f deployment/redis-leader
kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-service.yaml
kubectl get service

# --- Redis followers ---
kubectl apply -f https://k8s.io/examples/application/guestbook/redis-follower-deployment.yaml
kubectl get pods
kubectl apply -f https://k8s.io/examples/application/guestbook/redis-follower-service.yaml
kubectl get service

# --- PHP frontend ---
kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-deployment.yaml
kubectl get pods -l app=guestbook -l tier=frontend
kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-service.yaml
kubectl get services

# --- Access locally via port-forward ---
kubectl port-forward svc/frontend 8080:80
# Open http://localhost:8080 in browser

# --- Access via LoadBalancer (if manifest uncommented) ---
kubectl get service frontend   # wait for EXTERNAL-IP

# --- Scale frontend ---
kubectl scale deployment frontend --replicas=5
kubectl get pods
kubectl scale deployment frontend --replicas=2

# --- Cleanup (label-based, deletes multiple resources at once) ---
kubectl delete deployment -l app=redis
kubectl delete service -l app=redis
kubectl delete deployment frontend
kubectl delete service frontend
kubectl get pods   # should show no resources
```

## Prerequisites

- A Kubernetes cluster (minikube recommended; at least 2 worker nodes)
- `kubectl` configured against the cluster
- Understanding of Deployments, Services, and scaling ([[deploy-app]], [[expose-app]], [[scale-app]])
- `kubectl` 1.14 or later (manifest uses `apps/v1`)

## Key Concepts

- **Multi-tier architecture**: each tier is an independent Deployment + Service pair; Services decouple tiers from each other's Pod IPs
- **DNS-based service discovery**: Pods resolve other Services by name via CoreDNS; no need for hardcoded IPs or environment variable ordering tricks (cf. [[connect-applications-service]])
- **`kubectl port-forward svc/<name> <local>:<remote>`**: tunnels a local port to a ClusterIP Service — useful for development without a cloud LB
- **Leader/follower Redis**: single write replica (leader) + multiple read replicas (followers); each gets its own Service for DNS
- **Label-based bulk delete**: `kubectl delete <type> -l <selector>` deletes all matching resources in one command
- **ClusterIP default**: Services are not externally reachable by default; port-forward or LoadBalancer type required for external access

## Cross-references

- [[expose-app]] — Service types; ClusterIP vs NodePort vs LoadBalancer
- [[expose-external-ip]] — LoadBalancer Service with cloud provisioning
- [[scale-app]] — `kubectl scale` mechanics
- [[configure-redis-configmap]] — ConfigMap pattern used for Redis config in similar setups
- [[connect-applications-service]] — DNS discovery, EndpointSlices, TLS Secrets
- [[kubernetes-topic-taxonomy]] — `service`, `port-forward`, `dns`, `labels` domains

## Sources

- `docs/wiki/raw/tutorials/guestbook.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/stateless-application/guestbook/
