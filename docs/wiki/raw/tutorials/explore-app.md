# Viewing Pods and Nodes

Source: https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/
Fetched: 2026-08-07

---

## Objectives

- Learn about Kubernetes Pods.
- Learn about Kubernetes Nodes.
- Troubleshoot deployed applications.

---

## Before You Begin

- POSIX shell (bash, zsh, sh). Windows → WSL or Git Bash.
- Assumes the Deployment from Tutorial #2 (Deploy an App) is already running.

---

## Key Concepts

### Kubernetes Pods

A Pod is a Kubernetes abstraction representing a group of one or more application containers plus shared resources:
- Shared storage (Volumes)
- A unique cluster IP address
- Configuration for how to run each container (image version, ports, etc.)

Pods are the atomic unit of Kubernetes. A Deployment creates Pods (not containers directly). Each Pod is tied to the Node it is scheduled on and remains there until termination or deletion. On Node failure, identical Pods are rescheduled on other Nodes.

Containers in a Pod share an IP address and port space, are co-located and co-scheduled, and run in a shared context on the same Node.

### Nodes

A Node is a worker machine (physical or virtual), managed by the control plane. Every Node runs:
- **kubelet** — communicates between the control plane and the Node; manages Pods and containers.
- **Container runtime** (e.g., Docker/containerd) — pulls images, unpacks, and runs containers.

### kubectl Troubleshooting Commands

- `kubectl get` — list resources
- `kubectl describe` — detailed information about a resource (human-readable, not for scripting)
- `kubectl logs` — print logs from a container in a pod
- `kubectl exec` — execute a command on a container in a pod

---

## Commands

```bash
# List running pods
kubectl get pods

# Show detailed info about all pods (IP, ports, events, lifecycle)
kubectl describe pods

# Start proxy to access private network (second terminal)
kubectl proxy

# Capture pod name
export POD_NAME="$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\\n"}}{{end}}')"
echo Name of the Pod: $POD_NAME

# Access Pod via proxy
curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME:8080/proxy/

# List environment variables in the container
kubectl exec "$POD_NAME" -- env

# Open an interactive bash session inside the container
kubectl exec -ti $POD_NAME -- bash

# (inside the container) view the app source
cat server.js

# (inside the container) curl the app directly
curl http://localhost:8080

# Exit the container shell
exit
```

---

## Notes

- `kubectl describe` works on Nodes, Pods, Deployments, and most Kubernetes primitives.
- `kubectl exec` targets a single container; if the pod has only one container, `--container` flag can be omitted.
- Inside a container, `localhost` refers to the container's loopback interface.
- Pods run on a private network; proxy is needed for external access until a Service is created.
