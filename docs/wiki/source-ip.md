---
type: concept
title: Using Source IP
description: How source IP NAT behaves across ClusterIP, NodePort, and LoadBalancer Service types, how externalTrafficPolicy:Local preserves client IP at the cost of availability, and the healthCheckNodePort mechanism.
resource: https://kubernetes.io/docs/tutorials/services/source-ip/
tags: [source-ip, nat, kube-proxy, nodeport, loadbalancer, external-traffic-policy, healthcheck, networking]
timestamp: 2026-08-07T00:00:00Z
---

# Using Source IP

This tutorial demystifies how kube-proxy and cloud load balancers handle the source IP of packets as they traverse different Service types. The answer differs by Service type, and the tradeoff when preserving source IP is availability.

## Source NAT behaviour by Service type

### ClusterIP — no source NAT
Packets from a Pod to a ClusterIP Service are **never source NAT'd** in iptables mode (the default). The backend Pod sees the originating Pod's real IP as `client_address`. This is true whether the client and server Pods are on the same node or different nodes, because kube-proxy rewrites only the destination, not the source.

### NodePort — source NAT by default
When a packet arrives at `NodeIP:NodePort`, kube-proxy may forward it to an endpoint Pod on a **different node**. To ensure the reply can route back correctly, kube-proxy replaces the client's source IP with the node's IP (SNAT). The backend Pod sees the **node IP** as the client address, not the original client.

**To preserve source IP:** set `externalTrafficPolicy: Local`. kube-proxy then only routes to endpoints on the **local node**. If the node has no local endpoint, the packet is **dropped** (not forwarded). This gives accurate client IPs but risks dropped traffic — clients must connect to a node that happens to run an endpoint Pod.

### LoadBalancer — source NAT by default
Same as NodePort: cloud LBs distribute traffic across all nodes, and kube-proxy does SNAT when forwarding cross-node. With `externalTrafficPolicy: Local`, nodes with no endpoints **fail the health check** at `healthCheckNodePort`, so the cloud LB removes them from its pool automatically. This avoids packet drops at the cost of a less even load distribution.

## externalTrafficPolicy: Local details

- Auto-allocates a `healthCheckNodePort` (high-numbered port) on each node
- The LB polls each node at `<nodeIP>:<healthCheckNodePort>/healthz`
- Nodes with endpoints return `1 Service Endpoints found`; nodes without return `No Service Endpoints Found`
- The LB only routes traffic to nodes that pass this health check

## Key Commands

```bash
# Deploy the echo server
kubectl create deployment source-ip-app --image=registry.k8s.io/echoserver:1.10

# --- ClusterIP (no SNAT) ---
kubectl expose deployment source-ip-app --name=clusterip --port=80 --target-port=8080
# Test from inside a Pod:
kubectl run busybox -it --image=busybox:1.28 --restart=Never --rm
# Inside: wget -qO - <ClusterIP>   → client_address = your pod's real IP

# --- NodePort (SNAT by default) ---
kubectl expose deployment source-ip-app --name=nodeport --port=80 --target-port=8080 --type=NodePort
NODEPORT=$(kubectl get -o jsonpath="{.spec.ports[0].nodePort}" services nodeport)
NODES=$(kubectl get nodes -o jsonpath='{ $.items[*].status.addresses[?(@.type=="InternalIP")].address }')
for node in $NODES; do curl -s $node:$NODEPORT | grep -i client_address; done
# Shows node IPs (SNAT), not real client IP

# Preserve source IP on NodePort (drops packets if no local endpoint):
kubectl patch svc nodeport -p '{"spec":{"externalTrafficPolicy":"Local"}}'
for node in $NODES; do curl --connect-timeout 1 -s $node:$NODEPORT | grep -i client_address; done
# One reply with real client IP (from node with endpoint); others time out

# --- LoadBalancer (SNAT by default) ---
kubectl expose deployment source-ip-app --name=loadbalancer --port=80 --target-port=8080 --type=LoadBalancer
kubectl get svc loadbalancer   # wait for EXTERNAL-IP
curl <EXTERNAL-IP>             # client_address = node IP (SNAT)

# Preserve source IP on LoadBalancer (LB health-checks nodes):
kubectl patch svc loadbalancer -p '{"spec":{"externalTrafficPolicy":"Local"}}'
kubectl get svc loadbalancer -o yaml | grep -i healthCheckNodePort
# Nodes with endpoints: curl localhost:<healthCheckNodePort>/healthz → "1 Service Endpoints found"
curl <EXTERNAL-IP>             # now shows real client IP

# Check kube-proxy mode on a node
curl http://localhost:10249/proxyMode   # (run on the node) → "iptables"

# Cleanup
kubectl delete svc -l app=source-ip-app
kubectl delete deployment source-ip-app
```

## Prerequisites

- A cluster with at least 2 worker nodes (to observe cross-node SNAT)
- A cloud provider or equivalent for LoadBalancer type (or minikube with LoadBalancer support)
- Familiarity with Service types ([[expose-app]], [[expose-external-ip]])

## Key Concepts

- **Source NAT (SNAT)**: kube-proxy rewrites the packet's source IP to the node IP when forwarding cross-node; makes the reply routable but hides the original client IP
- **`externalTrafficPolicy: Local`**: disables cross-node forwarding; only routes to local endpoint Pods; preserves client IP but packets are dropped (NodePort) or health-check-gated (LoadBalancer) on nodes without endpoints
- **`healthCheckNodePort`**: auto-allocated port; cloud LB polls `/healthz` on each node; removes nodes without endpoints from LB rotation — automatic endpoint-based LB member management
- **iptables mode**: the default kube-proxy mode; performs DNAT (destination rewrite) for ClusterIP traffic; no SNAT within the cluster
- **Cloud LB types**: proxy-mode LBs always show the LB IP as source (no preservation possible); packet-forwarder LBs can preserve with `externalTrafficPolicy: Local`

## Cross-references

- [[expose-app]] — NodePort basics; `kubectl expose` and Service types
- [[expose-external-ip]] — LoadBalancer Service provisioning on cloud providers
- [[connect-applications-service]] — ClusterIP networking; kube-proxy; EndpointSlices
- [[pods-and-endpoint-termination-flow]] — endpoint conditions; how the LB knows endpoints are healthy
- [[kubernetes-topic-taxonomy]] — `source-ip`, `nat`, `kube-proxy`, `external-traffic-policy` domains

## Sources

- `docs/wiki/raw/tutorials/source-ip.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/services/source-ip/
