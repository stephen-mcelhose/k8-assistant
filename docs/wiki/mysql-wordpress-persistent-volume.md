---
type: concept
title: WordPress and MySQL with Persistent Volumes
description: Deploy a two-tier WordPress+MySQL application using Kustomize — Secret generator for credentials, PVCs for persistent data, Recreate deployment strategy, and kubectl apply -k for multi-resource management.
resource: https://kubernetes.io/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/
tags: [wordpress, mysql, kustomize, pvc, secret, deployment, recreate, stateful]
timestamp: 2026-08-07T00:00:00Z
---

# WordPress and MySQL with Persistent Volumes

This tutorial deploys a classic two-tier web application (MySQL + WordPress) on minikube using **Kustomize** — Kubernetes' built-in configuration management tool. It introduces three concepts not covered in earlier tutorials: Secret generators, the `Recreate` deployment strategy, and `kubectl apply -k`.

**Kustomize and the Secret generator:** A `kustomization.yaml` file declares all resources for the application. The `secretGenerator` block creates a Kubernetes Secret containing the MySQL root password; Kustomize appends a content hash to the Secret name (e.g., `mysql-pass-c57bb4t7mf`) to force Pod restarts when secrets change. Both MySQL and WordPress Deployments reference this Secret via `secretKeyRef`. Running `kubectl apply -k ./` applies all resources in the kustomization directory as a single atomic unit.

**Persistent storage:** Both tiers use 20 GiB PersistentVolumeClaims, dynamically provisioned by the default StorageClass. MySQL mounts at `/var/lib/mysql`; WordPress mounts at `/var/www/html`. Data survives Pod restarts and rescheduling — but on minikube with the `hostPath` provisioner, data is tied to the node's `/tmp` directory and is lost if the Pod migrates to a different node or the node reboots.

**`Recreate` strategy:** Both Deployments use `strategy: type: Recreate` instead of the default `RollingUpdate`. This terminates the existing Pod completely before starting the replacement. Essential for single-instance stateful applications where two instances of MySQL sharing the same PVC would cause data corruption.

**Service topology:** MySQL uses a headless `ClusterIP: None` Service named `wordpress-mysql` — WordPress discovers it by DNS name via the env var `WORDPRESS_DB_HOST=wordpress-mysql`. WordPress uses a `LoadBalancer` Service (on minikube, access via `minikube service wordpress --url` since minikube only supports NodePort externally).

> ⚠️ This deployment is not production-ready — single-instance MySQL and WordPress are not highly available. For production, use the WordPress Helm chart.

## Key Commands

```bash
# Create kustomization.yaml with Secret generator
cat <<EOF >./kustomization.yaml
secretGenerator:
- name: mysql-pass
  literals:
  - password=YOUR_PASSWORD
EOF

# Download manifests
curl -LO https://k8s.io/examples/application/wordpress/mysql-deployment.yaml
curl -LO https://k8s.io/examples/application/wordpress/wordpress-deployment.yaml

# Add resources to kustomization.yaml
cat <<EOF >>./kustomization.yaml
resources:
  - mysql-deployment.yaml
  - wordpress-deployment.yaml
EOF

# Apply everything
kubectl apply -k ./

# Verify
kubectl get secrets           # mysql-pass-<hash>
kubectl get pvc               # mysql-pv-claim and wp-pv-claim, Bound
kubectl get pods              # both Running
kubectl get services wordpress

# Access on minikube (LoadBalancer → NodePort on minikube)
minikube service wordpress --url

# Cleanup (deletes Secret, Deployments, Services, PVCs)
kubectl delete -k ./
```

## Prerequisites

- minikube (or another cluster with dynamic PV provisioning)
- kubectl 1.27+
- Understanding of PersistentVolumes and Services ([[basic-stateful-set]], [[expose-app]])

## Key Concepts

- **Kustomize**: built into kubectl since v1.14; `kustomization.yaml` defines resources, patches, Secret/ConfigMap generators; applied with `kubectl apply -k <dir>`
- **Secret generator**: Kustomize creates the Secret and appends a content hash to the name; avoids stale references when secrets rotate
- **`strategy: type: Recreate`**: terminates existing Pods before creating new ones; required for single-instance stateful workloads to avoid split-brain on shared storage
- **`ClusterIP: None` (headless) for MySQL**: single-instance DB doesn't need load balancing; headless Service provides DNS resolution only
- **`secretKeyRef`**: injects a Secret value as an env var; the Secret must exist before the Pod starts
- **`kubectl apply -k ./`**: applies all resources in the kustomization directory; `kubectl delete -k ./` removes them all
- **hostPath warning**: minikube's default StorageClass uses `hostPath`; data is not portable across nodes

## Cross-references

- [[basic-stateful-set]] — PVC lifecycle; `volumeClaimTemplates`; PVCs surviving Pod deletion
- [[cassandra]] — another stateful app with PVCs and explicit cleanup requirements
- [[configure-redis-configmap]] — Secret and ConfigMap patterns for configuration
- [[connect-applications-service]] — Service DNS discovery (`WORDPRESS_DB_HOST=wordpress-mysql`)
- [[expose-app]] — Service types; LoadBalancer vs NodePort
- [[kubernetes-topic-taxonomy]] — `kustomize`, `pvc`, `secret`, `recreate` domains

## Sources

- `docs/wiki/raw/tutorials/mysql-wordpress-persistent-volume.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/
