---
type: concept
title: Configuring Redis using a ConfigMap
description: How to mount a ConfigMap as a file volume inside a Pod, and why ConfigMap changes require a Pod restart to take effect — demonstrated with Redis maxmemory settings.
resource: https://kubernetes.io/docs/tutorials/configuration/configure-redis-using-configmap/
tags: [configmap, volume, exec, redis, configuration, pod, restart]
timestamp: 2026-08-07T00:00:00Z
---

# Configuring Redis using a ConfigMap

This tutorial demonstrates the standard pattern for externalising application configuration: store it in a **ConfigMap**, mount it as a file inside the Pod, and have the application read it on startup. The example uses Redis's `redis.conf` file to set `maxmemory` and `maxmemory-policy`.

The ConfigMap is first created empty (the `redis-config` key has no value). The Redis Pod manifest maps that key to a file at `/redis-master/redis.conf` via a volume: `spec.volumes[*].configMap` names the ConfigMap; `items[*].key` / `items[*].path` map the key to the filename; and `spec.containers[*].volumeMounts` mounts the volume into the container. The Redis server starts with `redis-server /redis-master/redis.conf`, so it reads the mounted file.

The critical lesson is **when ConfigMap changes take effect**: updating the ConfigMap with `kubectl apply` does not restart the Pod. Redis continues running with its previous (default) configuration. Only after `kubectl delete pod redis` and recreating the Pod does Redis re-read the updated file — confirmed by `redis-cli CONFIG GET maxmemory` returning `2097152` (2 MB) instead of `0`. This restart-required behaviour applies broadly: environment variables injected from ConfigMaps also require a Pod restart, while volume-mounted ConfigMaps _do_ update in-place (with a delay) in more recent Kubernetes versions — but applications still need to detect and reload the change.

## Key Commands

```bash
# Create an empty ConfigMap
cat <<EOF > ./example-redis-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: example-redis-config
data:
  redis-config: ""
EOF
kubectl apply -f example-redis-config.yaml

# Deploy Redis Pod that mounts the ConfigMap
kubectl apply -f https://raw.githubusercontent.com/kubernetes/website/main/content/en/examples/pods/config/redis-pod.yaml

# Verify Pod and ConfigMap are running
kubectl get pod/redis configmap/example-redis-config

# Inspect the ConfigMap (initially empty)
kubectl describe configmap/example-redis-config

# Check Redis defaults via redis-cli
kubectl exec -it pod/redis -- redis-cli
# Inside redis-cli:
# CONFIG GET maxmemory        → 0
# CONFIG GET maxmemory-policy → noeviction

# Update the ConfigMap with real values
# (edit example-redis-config.yaml: set redis-config to "maxmemory 2mb\nmaxmemory-policy allkeys-lru")
kubectl apply -f example-redis-config.yaml
kubectl describe configmap/example-redis-config   # confirm update

# ConfigMap updated — but Pod still uses old values:
kubectl exec -it pod/redis -- redis-cli
# CONFIG GET maxmemory → still 0  (Pod must restart)

# Restart the Pod to pick up new config
kubectl delete pod redis
kubectl apply -f https://raw.githubusercontent.com/kubernetes/website/main/content/en/examples/pods/config/redis-pod.yaml

# Verify new values took effect
kubectl exec -it pod/redis -- redis-cli
# CONFIG GET maxmemory        → 2097152 (2 MB)
# CONFIG GET maxmemory-policy → allkeys-lru

# Clean up
kubectl delete pod/redis configmap/example-redis-config
```

## Prerequisites

- A Kubernetes cluster (minikube works; tutorial recommends 2 worker nodes)
- `kubectl` 1.14 or later
- Familiarity with Pods and `kubectl exec` ([[explore-app]])

## Key Concepts

- **ConfigMap**: a Kubernetes object that stores non-secret configuration data as key-value pairs; decouples config from container images
- **Volume mount (ConfigMap)**: `spec.volumes[*].configMap` + `spec.containers[*].volumeMounts` makes ConfigMap keys available as files inside the container
- **`items[*].key` / `items[*].path`**: controls which ConfigMap key maps to which filename on the volume
- **Restart required**: updating a ConfigMap does not restart Pods or reload configuration in running processes — the Pod must be deleted and recreated (or the application must implement config-reload logic)
- **`kubectl exec -it <pod> -- <cmd>`**: runs an interactive command inside a running container; used here to invoke `redis-cli` for verification

## Cross-references

- [[explore-app]] — `kubectl exec` for inspecting Pod internals
- [[guestbook]] — ConfigMap and volume patterns at multi-tier scale
- [[connect-applications-service]] — using ConfigMap to store nginx TLS config
- [[kubernetes-topic-taxonomy]] — `configmap`, `volume`, `exec` domains

## Sources

- `docs/wiki/raw/tutorials/configure-redis-configmap.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/configuration/configure-redis-using-configmap/
