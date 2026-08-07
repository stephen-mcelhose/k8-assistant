---
type: concept
title: Expose Your App Publicly (Service + NodePort)
description: How Kubernetes Services provide stable virtual IPs over ephemeral Pods, how to expose a Deployment with NodePort on minikube, and how labels/selectors connect Services to Pods.
resource: https://kubernetes.io/docs/tutorials/kubernetes-basics/expose/expose-intro/
tags: [service, nodeport, selector, labels, expose, clusterip, loadbalancer, externalname, basics]
timestamp: 2026-08-07T00:00:00Z
---

# Expose Your App Publicly (Service + NodePort)

Pods are ephemeral — they die and are replaced with new IPs whenever a Node fails or a rolling update occurs. A **Service** solves this by defining a stable virtual IP (ClusterIP) and DNS name that front a dynamic set of Pods matched by a label selector. Traffic to the Service is automatically load-balanced across all matching Pods. The tutorial introduces all four Service types (ClusterIP, NodePort, LoadBalancer, ExternalName) but focuses on NodePort as the mechanism for exposing an application outside the cluster on minikube.

`kubectl expose deployment` is the imperative shorthand: it reads the Deployment's Pod template labels, creates a matching selector, and writes the Service object. The resulting Service gets a ClusterIP for internal use and, for NodePort type, a high-numbered port (30000–32767) on every Node. On minikube, `$(minikube ip):$NODE_PORT` routes to the application. On Docker Desktop with minikube, a tunnel is needed: `minikube service <name> --url` instead.

The tutorial also teaches **labels** as a first-class operational tool. Labels are key/value pairs on any object; `kubectl get` and `kubectl delete` both accept `-l <selector>` to filter. `kubectl label pods $POD_NAME version=v1` attaches a new label to a running Pod. This is the mechanism Services use: when you change a Pod's labels so they no longer match the Service selector, the Service stops routing to it — a useful debugging technique.

A critical point: **deleting a Service does not stop the application**. The Deployment continues managing its Pods; the Service is just the routing layer. To stop the app, delete the Deployment separately.

## Key Commands

```bash
# Check Pods are running (prerequisite: deployment from deploy-app tutorial)
kubectl get pods
kubectl get services

# Expose the deployment as a NodePort Service
kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080

# Find the NodePort assigned
kubectl describe services/kubernetes-bootcamp

# Capture NodePort in an env variable
export NODE_PORT="$(kubectl get services/kubernetes-bootcamp \
  -o go-template='{{(index .spec.ports 0).nodePort}}')"
echo "NODE_PORT=$NODE_PORT"

# Access the app (standard minikube)
curl http://"$(minikube ip):$NODE_PORT"

# Access the app (minikube with Docker Desktop driver — run in separate terminal)
minikube service kubernetes-bootcamp --url

# Inspect Deployment labels
kubectl describe deployment

# Filter Pods by label
kubectl get pods -l app=kubernetes-bootcamp
kubectl get services -l app=kubernetes-bootcamp

# Capture Pod name
export POD_NAME="$(kubectl get pods -o go-template \
  --template '{{range .items}}{{.metadata.name}}{{"\\n"}}{{end}}')"

# Add a label to a Pod
kubectl label pods "$POD_NAME" version=v1
kubectl describe pods "$POD_NAME"
kubectl get pods -l version=v1

# Delete a Service by label
kubectl delete service -l app=kubernetes-bootcamp

# Verify Service is gone (app still runs — Deployment is separate)
kubectl get services
curl http://"$(minikube ip):$NODE_PORT"          # now fails
kubectl exec -ti $POD_NAME -- curl http://localhost:8080  # still works
```

## Prerequisites

- A running Deployment from [[deploy-app]] (`kubernetes-bootcamp`)
- minikube running locally (or equivalent cluster)
- Understanding of Pods and Nodes ([[explore-app]])

## Key Concepts

- **Service**: stable virtual IP + DNS name fronting a dynamic set of Pods via label selector; survives Pod restarts and rescheduling
- **ClusterIP**: default type — cluster-internal only; not reachable from outside
- **NodePort**: opens the same high port on every Node; externally reachable via `NodeIP:NodePort`; superset of ClusterIP
- **LoadBalancer**: provisions a cloud LB with external IP; see [[expose-external-ip]]; superset of NodePort
- **ExternalName**: CNAME alias to an external DNS name; no proxying
- **Label selector**: the mechanism Services use to find their Pods — match on `key=value` pairs
- **Deleting a Service ≠ stopping the app**: the Deployment keeps running; delete the Deployment to stop Pods

## Cross-references

- [[deploy-app]] — creates the Deployment this tutorial exposes
- [[scale-app]] — scaling the Deployment behind the Service
- [[update-app]] — rolling updates while the Service remains live
- [[expose-external-ip]] — LoadBalancer alternative for cloud environments
- [[connect-applications-service]] — deep dive into Service DNS, ClusterIP, and EndpointSlices
- [[kubernetes-topic-taxonomy]] — `service`, `nodeport`, `selector`, `labels` domains

## Sources

- `docs/wiki/raw/tutorials/expose-app.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/kubernetes-basics/expose/expose-intro/
