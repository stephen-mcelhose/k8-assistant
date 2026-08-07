---
type: concept
title: Apply Pod Security Standards at the Cluster Level
description: How to configure cluster-wide Pod Security Standards via AdmissionConfiguration passed to the API server — using dry-run assessment, kube-system exemption, and kind with kubeadmConfigPatches. Contrasted with namespace-level label approach.
resource: https://kubernetes.io/docs/tutorials/security/cluster-level-pss/
tags: [pod-security, pss, admission-controller, cluster-level, kind, kubeadm, kube-system]
timestamp: 2026-08-07T00:00:00Z
---

# Apply Pod Security Standards at the Cluster Level

**Cluster-level PSS** configures Pod Security Standards as API server defaults that apply to every namespace in the cluster — unlike [[ns-level-pss]] which applies policy one namespace at a time via labels. Because the configuration is passed to the API server at startup, **this approach requires control over the control plane** and is not available on managed clusters (GKE, EKS, AKS). Use namespace labels instead for managed clusters.

## How it works

An `AdmissionConfiguration` file is written to the control plane node and referenced by the API server via `--admission-control-config-file`. It configures the `PodSecurity` admission plugin with default modes and levels that apply to all namespaces not explicitly exempted.

```yaml
# /tmp/pss/cluster-level-pss.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: PodSecurity
  configuration:
    apiVersion: pod-security.admission.config.k8s.io/v1
    kind: PodSecurityConfiguration
    defaults:
      enforce: "baseline"
      enforce-version: "latest"
      audit: "restricted"
      audit-version: "latest"
      warn: "restricted"
      warn-version: "latest"
    exemptions:
      usernames: []
      runtimeClasses: []
      namespaces: [kube-system]
```

**Why exempt `kube-system`?** kube-system Pods (etcd, kindnet, kube-proxy) use host namespaces, hostPath volumes, and privileged capabilities — all of which violate even the `baseline` PSS level. Without exemption, enforcing baseline cluster-wide would block kube-system Pods from (re)starting.

## Choosing levels: the dry-run assessment

Before enforcing any standard, use `--dry-run=server` to see which namespaces would emit warnings:

```bash
# Privileged: no warnings anywhere (expected)
kubectl label --dry-run=server --overwrite ns --all \
  pod-security.kubernetes.io/enforce=privileged

# Baseline: warnings only for kube-system (host namespaces, hostPath, capabilities)
kubectl label --dry-run=server --overwrite ns --all \
  pod-security.kubernetes.io/enforce=baseline

# Restricted: warnings for kube-system AND local-path-storage
kubectl label --dry-run=server --overwrite ns --all \
  pod-security.kubernetes.io/enforce=restricted
```

The recommended production strategy: **enforce=baseline** (blocks known privilege escalations; kube-system exempted), **warn+audit=restricted** (surfaces restricted violations without blocking — operators learn what needs hardening).

## Key Commands

```bash
# Step 1: write the AdmissionConfiguration
mkdir -p /tmp/pss
cat <<EOF > /tmp/pss/cluster-level-pss.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: PodSecurity
  configuration:
    apiVersion: pod-security.admission.config.k8s.io/v1
    kind: PodSecurityConfiguration
    defaults:
      enforce: "baseline"
      enforce-version: "latest"
      audit: "restricted"
      audit-version: "latest"
      warn: "restricted"
      warn-version: "latest"
    exemptions:
      namespaces: [kube-system]
EOF

# Step 2: write the kind cluster config that mounts and references the file
cat <<EOF > /tmp/pss/cluster-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: ClusterConfiguration
    apiServer:
      extraArgs:
        admission-control-config-file: /etc/config/cluster-level-pss.yaml
      extraVolumes:
      - name: accf
        hostPath: /etc/config
        mountPath: /etc/config
  extraMounts:
  - hostPath: /tmp/pss
    containerPath: /etc/config
EOF

# Step 3: create the cluster (takes ~2 min)
kind create cluster --name psa-with-cluster-pss --config /tmp/pss/cluster-config.yaml
kubectl cluster-info --context kind-psa-with-cluster-pss

# Step 4: test — baseline-compliant Pod in default namespace
# Creates successfully but warns about restricted violations
kubectl apply -f https://k8s.io/examples/security/example-baseline-pod.yaml

# Cleanup
kind delete cluster --name psa-with-cluster-pss
```

## Prerequisites

- `kind` and `kubectl` installed
- Full control over the cluster's API server configuration (not available on managed clusters)
- Kubernetes v1.25+ (`pod-security.admission.config.k8s.io/v1`; use `v1beta1` for v1.23-1.24)

## Key Concepts

- **`AdmissionConfiguration`**: an API server config file (not a Kubernetes object) that configures admission plugins; passed via `--admission-control-config-file` flag
- **Cluster defaults vs namespace labels**: cluster defaults set a floor; namespace labels can be more or less restrictive on a per-namespace basis and override the cluster default
- **`exemptions.namespaces`**: namespaces listed here bypass all PSS checks entirely; use sparingly and with compensating access controls
- **`enforce-version: "latest"`**: evaluates against the current Kubernetes version's PSS definition; pin to a specific version (e.g., `"v1.30"`) to prevent policy drift on cluster upgrade
- **Dry-run pattern**: essential before applying cluster-wide policy; `--dry-run=server` shows warnings without mutating anything

## Cross-references

- [[ns-level-pss]] — namespace-level PSS via labels; the approach for managed clusters and per-namespace customization
- [[apparmor]] — AppArmor profiles referenced by `restricted` PSS level
- [[seccomp]] — seccomp `RuntimeDefault` required by `restricted` PSS level
- [[kubernetes-topic-taxonomy]] — `pod-security`, `pss`, `admission-controller`, `cluster-level` domains

## Sources

- `docs/wiki/raw/tutorials/cluster-level-pss.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/security/cluster-level-pss/
