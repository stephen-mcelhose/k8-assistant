---
type: concept
title: Updating Configuration via a ConfigMap
description: Four ConfigMap update scenarios — volume-mounted (auto-propagates), env var (requires rollout restart), multi-container shared volume, sidecar container — plus immutable ConfigMaps.
resource: https://kubernetes.io/docs/tutorials/configuration/updating-configuration-via-a-configmap/
tags: [configmap, volume, env-var, rollout, sidecar, immutable, port-forward, configuration]
timestamp: 2026-08-07T00:00:00Z
---

# Updating Configuration via a ConfigMap

This tutorial is a direct sequel to [[configure-redis-configmap]], covering four concrete update scenarios with a critical distinction at its core: **how and when** a ConfigMap change reaches a running container depends on how the ConfigMap is consumed.

## The four scenarios

**1. Volume-mounted ConfigMap (auto-propagates):** When a ConfigMap is mounted as a volume, the kubelet periodically syncs the mounted files. After `kubectl edit configmap <name>`, the updated value appears in the container's filesystem within one kubelet sync period — no Pod restart needed. However, the **application** must actively poll or watch the file for the change to take effect; a process that reads config only at startup will not notice.

**2. Environment variable (requires rollout restart):** When a ConfigMap value is injected as an env var (`valueFrom.configMapKeyRef`), changes to the ConfigMap do **not** update the running process. Environment variables are set at container start and are immutable for the lifetime of that container. To apply an update: `kubectl rollout restart deployment <name>`, which triggers a rolling replacement of all Pods. New Pods start with the updated env var; until the rollout completes, old and new Pods may co-exist with different values.

**3. Multi-container Pod with shared emptyDir:** A helper container reads the ConfigMap volume and writes an `index.html` to a shared `emptyDir`; a web server container reads from the same emptyDir. Because the helper reads the volume file, ConfigMap updates propagate to the shared dir (within kubelet sync), and the web server picks up the change on its next read cycle — no restart.

**4. Native sidecar container:** Identical to scenario 3 but uses an `initContainer` with `restartPolicy: Always` (a native sidecar) instead of a regular container. The sidecar is guaranteed to start before the main container. See [[pod-sidecar-containers]] for native sidecar adoption details.

**Immutable ConfigMaps:** Setting `immutable: true` on a ConfigMap prevents any further changes. The kubelet stops watching for updates (a performance optimisation). To change the configuration: create a new ConfigMap with a new name, then `kubectl edit deployment` to update the volume reference. The old ConfigMap can then be deleted. Immutability cannot be reversed — once set, the field cannot be removed.

## Key Commands

```bash
# --- Scenario 1: volume-mounted ---
kubectl create configmap sport --from-literal=sport=football
kubectl apply -f https://k8s.io/examples/deployments/deployment-with-configmap-as-volume.yaml
kubectl get pods --selector=app.kubernetes.io/name=configmap-volume
kubectl logs deployments/configmap-volume
# Edit the configmap and watch logs update automatically:
kubectl edit configmap sport
kubectl logs deployments/configmap-volume --follow

# --- Scenario 2: environment variable ---
kubectl create configmap fruits --from-literal=fruits=apples
kubectl apply -f https://k8s.io/examples/deployments/deployment-with-configmap-as-envvar.yaml
kubectl edit configmap fruits         # change apples → mangoes
kubectl logs deployments/configmap-env-var --follow   # stays "apples"
# Force update via rollout restart:
kubectl rollout restart deployment configmap-env-var
kubectl rollout status deployment configmap-env-var --watch=true
kubectl logs deployment/configmap-env-var             # now "mangoes"

# --- Scenario 3: multi-container + port-forward ---
kubectl create configmap color --from-literal=color=red
kubectl apply -f https://k8s.io/examples/deployments/deployment-with-configmap-two-containers.yaml
kubectl expose deployment configmap-two-containers --name=configmap-service --port=8080 --target-port=80
kubectl port-forward service/configmap-service 8080:8080 &
curl http://localhost:8080
kubectl edit configmap color          # change red → blue
while true; do curl --connect-timeout 7.5 http://localhost:8080; sleep 10; done  # watch it change

# --- Scenario 4: native sidecar ---
kubectl apply -f https://k8s.io/examples/deployments/deployment-with-configmap-and-sidecar-container.yaml
kubectl expose deployment configmap-sidecar-container --name=configmap-sidecar-service --port=8081 --target-port=80
kubectl port-forward service/configmap-sidecar-service 8081:8081 &

# --- Immutable ConfigMap ---
kubectl apply -f https://k8s.io/examples/configmap/immutable-configmap.yaml
kubectl apply -f https://k8s.io/examples/deployments/deployment-with-immutable-configmap-as-volume.yaml
# To change: create new ConfigMap, edit Deployment to reference it
kubectl apply -f https://k8s.io/examples/configmap/new-immutable-configmap.yaml
kubectl edit deployment immutable-configmap-volume    # update volumes[*].configMap.name
kubectl delete configmap company-name-20150801        # clean up old

# --- Full cleanup ---
kubectl delete deployment configmap-volume configmap-env-var configmap-two-containers \
  configmap-sidecar-container immutable-configmap-volume
kubectl delete service configmap-service configmap-sidecar-service
kubectl delete configmap sport fruits color company-name-20240312
```

## Prerequisites

- A Kubernetes cluster (minikube works; at least 2 worker nodes recommended)
- `curl` available locally for testing port-forward scenarios
- Familiarity with ConfigMaps and volume mounts ([[configure-redis-configmap]])

## Key Concepts

- **Volume-mounted ConfigMap → auto-propagates**: kubelet updates the mounted files within one sync period; app must poll/watch to react
- **Env var ConfigMap → requires pod restart**: env vars are fixed at container start; use `kubectl rollout restart` to apply changes
- **`kubectl edit configmap`**: opens `$EDITOR` for inline ConfigMap edits
- **`kubectl rollout restart deployment`**: triggers a rolling replacement of all Pods in the Deployment
- **`immutable: true`**: prevents further changes; kubelet stops watching for updates; requires new ConfigMap + Deployment edit to change
- **`kubectl port-forward svc/<name> <local>:<remote> &`**: background port tunnel for local testing without a LoadBalancer

## Cross-references

- [[configure-redis-configmap]] — foundational ConfigMap volume mount tutorial (restart-required baseline)
- [[pod-sidecar-containers]] — native sidecar containers used in scenario 4
- [[update-app]] — `kubectl rollout restart` / `kubectl rollout status` mechanics
- [[guestbook]] — `kubectl port-forward` for local service access
- [[kubernetes-topic-taxonomy]] — `configmap`, `volume`, `env-var`, `rollout`, `sidecar` domains

## Sources

- `docs/wiki/raw/tutorials/updating-configuration-via-a-configmap.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/configuration/updating-configuration-via-a-configmap/
