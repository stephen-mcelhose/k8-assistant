---
type: concept
title: Connecting Applications with Services
description: Deep dive into Kubernetes Service networking — ClusterIP, EndpointSlices, environment variable vs DNS discovery, ordering pitfalls, TLS Secrets, ConfigMaps for nginx config, and switching to LoadBalancer.
resource: https://kubernetes.io/docs/tutorials/services/connect-applications-service/
tags: [service, dns, coredns, clusterip, endpointslice, tls, secret, configmap, nodeport, loadbalancer, networking]
timestamp: 2026-08-07T00:00:00Z
---

# Connecting Applications with Services

This tutorial provides the deepest coverage of Services in the Basics series. It explains the Kubernetes networking model from first principles: every Pod gets a cluster-private IP with no NAT between Pods, but Pod IPs are ephemeral. Services solve this by providing a **stable ClusterIP** tied to the Service's lifetime — Pods talk to the ClusterIP, and kube-proxy routes traffic to a healthy Pod from the backing **EndpointSlice**.

The tutorial covers two Service discovery mechanisms:

1. **Environment variables**: the kubelet injects `<SERVICE_NAME>_SERVICE_HOST` and `<SERVICE_NAME>_SERVICE_PORT` into every Pod on the same Node — but only for Services that existed *before* the Pod started. This creates an ordering problem: if you create Pods before the Service, they get no env vars. The fix is to scale the Deployment to 0 and back to 2 after the Service exists, forcing Pod recreation.

2. **DNS (CoreDNS)**: the preferred mechanism. CoreDNS assigns `<service-name>.<namespace>.svc.cluster.local` to every Service; Pods resolve it with standard `gethostbyname()`. No ordering constraint. Verify with `kubectl run curl --image=radial/busyboxplus:curl -i --tty --rm` and `nslookup my-nginx` inside.

The tutorial then shows securing a Service with TLS: create a **Secret** (`kubectl create secret tls`) holding the cert and key, a **ConfigMap** for the nginx config file, and update the Deployment to mount both as volumes. The updated Service exposes both port 80 (HTTP) and port 443 (HTTPS) — a multi-port Service. Finally it walks through switching the Service from NodePort to **LoadBalancer** with `kubectl edit svc`, demonstrating in-place Service type change.

## Key Commands

```bash
# Deploy 2-replica nginx
kubectl apply -f ./run-my-nginx.yaml
kubectl get pods -l run=my-nginx -o wide
kubectl get pods -l run=my-nginx -o custom-columns=POD_IP:.status.podIPs

# Create ClusterIP Service
kubectl expose deployment/my-nginx
kubectl get svc my-nginx

# Inspect Service endpoints (backed by EndpointSlices)
kubectl describe svc my-nginx
kubectl get endpointslices -l kubernetes.io/service-name=my-nginx

# Demonstrate env var ordering problem: scale to 0 then back to 2
kubectl scale deployment my-nginx --replicas=0
kubectl scale deployment my-nginx --replicas=2
kubectl get pods -l run=my-nginx -o wide

# Verify env vars are now set
kubectl exec <pod-name> -- printenv | grep SERVICE

# DNS discovery: run a curl Pod and resolve the Service by name
kubectl run curl --image=radial/busyboxplus:curl -i --tty --rm
# Inside: nslookup my-nginx

# Check CoreDNS is running
kubectl get services kube-dns --namespace=kube-system

# Secure with TLS
make keys KEY=/tmp/nginx.key CERT=/tmp/nginx.crt
# or manually:
openssl req -x509 -noenc -days 365 -newkey rsa:2048 \
  -keyout /tmp/nginx.key -out /tmp/nginx.crt -subj "/CN=my-nginx/O=my-nginx"

kubectl create secret tls nginxsecret --key /tmp/nginx.key --cert /tmp/nginx.crt
kubectl get secrets

kubectl create configmap nginxconfigmap --from-file=default.conf
kubectl describe configmap nginxconfigmap

# Deploy secure nginx (Deployment + Service with ports 80 and 443)
kubectl delete deployments,svc my-nginx
kubectl create -f ./nginx-secure-app.yaml

# Test HTTPS from within cluster
kubectl get pods -l run=my-nginx -o custom-columns=POD_IP:.status.podIPs
curl -k https://<pod-ip>

# Test from a curl Pod with the TLS secret mounted
kubectl apply -f ./curlpod.yaml
kubectl exec <curl-pod> -- curl https://my-nginx --cacert /etc/nginx/ssl/tls.crt

# Switch Service type from NodePort to LoadBalancer
kubectl edit svc my-nginx   # change type: NodePort → type: LoadBalancer
kubectl get svc my-nginx    # wait for EXTERNAL-IP
curl https://<EXTERNAL-IP> -k
```

## Prerequisites

- A Kubernetes cluster with CoreDNS (standard in most distributions)
- `go` and `make` for TLS key generation (or use the manual `openssl` steps)
- Understanding of Deployments, Services, and Secrets ([[deploy-app]], [[expose-app]])

## Key Concepts

- **ClusterIP**: stable virtual IP assigned at Service creation; tied to Service lifetime; never hits the wire (kube-proxy handles routing)
- **EndpointSlice**: tracks live Pod IPs matching the Service selector; updated automatically as Pods come and go
- **Env var discovery**: `<NAME>_SERVICE_HOST` / `<NAME>_SERVICE_PORT` — requires Service to exist before Pod creation; disable with `enableServiceLinks: false`
- **DNS discovery**: CoreDNS resolves `<service>.<namespace>.svc.cluster.local`; preferred over env vars; no ordering constraint
- **TLS Secret** (`kubernetes.io/tls`): stores `tls.crt` and `tls.key`; volume-mounted into the nginx container at `/etc/nginx/ssl/`
- **ConfigMap for nginx config**: stores `default.conf`; volume-mounted at `/etc/nginx/conf.d/`
- **Multi-port Service**: a single Service can expose multiple ports (e.g., 80 HTTP and 443 HTTPS) with named port entries
- **`kubectl edit svc`**: opens the Service manifest in `$EDITOR` for in-place edits; changing `type` reconfigures the Service live
- **AWS note**: LoadBalancer on AWS gives a hostname (ELB), not an IP — use `kubectl describe service` to see the full hostname

## Cross-references

- [[expose-app]] — Service types overview; NodePort basics
- [[expose-external-ip]] — LoadBalancer Service walkthrough
- [[namespaces-walkthrough]] — DNS is namespace-aware (CoreDNS)
- [[configure-redis-configmap]] — ConfigMap volume mount pattern
- [[guestbook]] — DNS-based inter-tier discovery in practice
- [[kubernetes-topic-taxonomy]] — `service`, `dns`, `coredns`, `tls`, `secret`, `configmap` domains

## Sources

- `docs/wiki/raw/tutorials/connect-applications-service.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/services/connect-applications-service/
