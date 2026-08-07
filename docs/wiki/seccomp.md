---
type: concept
title: Restrict Container Syscalls with seccomp
description: How to load seccomp profiles into a kind cluster, apply them via securityContext.seccompProfile, progress from audit→violation→fine-grained profiles, and enable RuntimeDefault as the cluster-wide default. GA since v1.19.
resource: https://kubernetes.io/docs/tutorials/security/seccomp/
tags: [seccomp, syscall, security-context, kind, runtime-default, profile, linux, kernel]
timestamp: 2026-08-07T00:00:00Z
---

# Restrict Container Syscalls with seccomp

**seccomp** (secure computing mode) is a Linux kernel feature that filters the syscalls a process is allowed to make. Kubernetes has supported seccomp profiles since v1.19 (GA). Unlike AppArmor (MAC policy), seccomp operates purely at the syscall level — the most fundamental boundary between userspace and kernel.

The tutorial works through four profiles in ascending order of security, building an understanding of how to craft production-ready profiles:

1. **`RuntimeDefault`** — the container runtime's built-in allowlist; a safe default for most workloads
2. **`audit.json`** (`SCMP_ACT_LOG`) — logs every syscall to syslog, allows all; used to discover what syscalls an app actually needs
3. **`violation.json`** (`SCMP_ACT_ERRNO`) — blocks every syscall; Pod enters CrashLoopBackOff immediately; useful only to demonstrate enforcement
4. **`fine-grained.json`** — `SCMP_ACT_ERRNO` as default + explicit `SCMP_ACT_ALLOW` list derived from audit output; Pod runs cleanly with no syslog output

## Profile file loading with kind

seccomp profiles are JSON files that must be pre-loaded onto each node under `/var/lib/kubelet/seccomp/`. The tutorial uses `kind` with `extraMounts` to inject profiles into the kind node container at cluster creation:

```yaml
# kind.yaml
apiVersion: kind.x-k8s.io/v1alpha4
kind: Cluster
nodes:
- role: control-plane
  extraMounts:
  - hostPath: "./profiles"
    containerPath: "/var/lib/kubelet/seccomp/profiles"
```

This is the canonical approach for local development. In real clusters, use DaemonSets, the Security Profiles Operator, or node provisioning tooling.

## API

```yaml
# Pod or container securityContext
securityContext:
  seccompProfile:
    type: RuntimeDefault       # RuntimeDefault | Localhost | Unconfined
    localhostProfile: profiles/fine-grained.json  # only for Localhost; relative to /var/lib/kubelet/seccomp/
```

> ⚠️ Prior to v1.19 seccomp was configured via annotations. The GA API uses `securityContext.seccompProfile`.

## Key Commands

```bash
# Download profiles
mkdir ./profiles
curl -L -o profiles/audit.json https://k8s.io/examples/pods/security/seccomp/profiles/audit.json
curl -L -o profiles/violation.json https://k8s.io/examples/pods/security/seccomp/profiles/violation.json
curl -L -o profiles/fine-grained.json https://k8s.io/examples/pods/security/seccomp/profiles/fine-grained.json

# Create kind cluster with profiles mounted
curl -L -O https://k8s.io/examples/pods/security/seccomp/kind.yaml
kind create cluster --config=kind.yaml

# Verify profiles are available inside the node
docker exec -it kind-control-plane ls /var/lib/kubelet/seccomp/profiles

# --- RuntimeDefault (safe default) ---
kubectl apply -f https://k8s.io/examples/pods/security/seccomp/ga/default-pod.yaml
kubectl get pod default-pod
kubectl delete pod default-pod --wait --now

# --- Audit profile (logs all syscalls) ---
kubectl apply -f https://k8s.io/examples/pods/security/seccomp/ga/audit-pod.yaml
kubectl expose pod audit-pod --type NodePort --port 5678
kubectl get service audit-pod   # note NodePort
docker exec -it kind-control-plane curl localhost:<nodeport>
tail -f /var/log/syslog | grep 'http-echo'   # observe syscall audit entries

# --- Violation profile (blocks all → CrashLoopBackOff) ---
kubectl apply -f https://k8s.io/examples/pods/security/seccomp/ga/violation-pod.yaml
kubectl get pod violation-pod   # STATUS: CrashLoopBackOff

# --- Fine-grained profile (allowlist → no syslog output) ---
kubectl apply -f https://k8s.io/examples/pods/security/seccomp/ga/fine-pod.yaml
kubectl expose pod fine-pod --type NodePort --port 5678
docker exec -it kind-control-plane curl localhost:<nodeport>
# No syslog output = all needed syscalls allowed, nothing else

# --- Enable RuntimeDefault as cluster-wide default ---
# kubelet flag: --seccomp-default
# Or in kubelet config: seccompDefault: true
# Verify the default profile is applied to a new Pod:
kubectl run --rm -it --restart=Never --image=alpine alpine -- sh
docker exec -it kind-worker bash -c \
  'crictl inspect $(crictl ps --name=alpine -q) | jq .info.runtimeSpec.linux.seccomp'
```

## Prerequisites

- `kind` and `kubectl` installed
- Docker available (kind uses Docker containers as nodes)
- Linux host (seccomp is a Linux kernel feature; `/var/log/syslog` must be accessible)
- Kubernetes v1.19+ for GA seccompProfile API

## Key Concepts

- **`SCMP_ACT_LOG`**: log the syscall to syslog, allow it — used for audit/profiling, not enforcement
- **`SCMP_ACT_ERRNO`**: block the syscall, return error to the process — enforcement action
- **`SCMP_ACT_ALLOW`**: explicitly allow a syscall — used in the allowlist within a restrictive profile
- **`localhostProfile` path**: relative to `/var/lib/kubelet/seccomp/` on the node; e.g., `profiles/fine-grained.json` resolves to `/var/lib/kubelet/seccomp/profiles/fine-grained.json`
- **`--seccomp-default` kubelet flag**: enables `RuntimeDefault` as the global default for all Pods that don't specify a profile (GA v1.27); must be enabled per-node
- **Privileged containers**: always run `Unconfined` — seccomp cannot be applied to privileged containers
- **Profile authoring workflow**: `audit.json` → inspect syslog → extract syscall numbers → build fine-grained allowlist → validate with `fine-grained.json`

## Cross-references

- [[apparmor]] — complementary kernel-level security: AppArmor = MAC policy path/capability rules; seccomp = syscall filter
- [[ns-level-pss]] — `restricted` PSS level requires `RuntimeDefault` or custom seccomp profile
- [[pod-sidecar-containers]] — seccomp applies per-container; sidecars can carry their own profile
- [[kubernetes-topic-taxonomy]] — `seccomp`, `syscall`, `security-context`, `runtime-default` domains

## Sources

- `docs/wiki/raw/tutorials/seccomp.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/security/seccomp/
