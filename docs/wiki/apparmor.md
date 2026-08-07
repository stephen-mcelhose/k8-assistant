---
type: concept
title: Restrict Container Access with AppArmor
description: How to load AppArmor profiles onto nodes, apply them to Pods via securityContext.appArmorProfile, verify enforcement, and understand what happens when profiles are violated or missing. Stable GA since v1.31.
resource: https://kubernetes.io/docs/tutorials/security/apparmor/
tags: [apparmor, security-context, pod-security, linux, kernel, profile, node]
timestamp: 2026-08-07T00:00:00Z
---

# Restrict Container Access with AppArmor

**AppArmor** is a Linux kernel security module (stable GA in Kubernetes v1.31, enabled by default) that constrains what a container process is allowed to do — which files it can read or write, which syscalls it can make, and what network operations are permitted. Kubernetes applies AppArmor profiles at the container level via `securityContext`.

## Three prerequisites — all must be satisfied

1. **Kernel module enabled**: check `cat /sys/module/apparmor/parameters/enabled` — must return `Y`. Ubuntu and SUSE enable this by default.
2. **Container runtime support**: containerd and CRI-O both support AppArmor. The runtime must be configured for it.
3. **Profile loaded on the node**: the profile must exist in the kernel (`/sys/kernel/security/apparmor/profiles`) on the node where the Pod will run. If the profile is missing, the kubelet rejects the Pod.

There is no built-in Kubernetes mechanism to distribute profiles to nodes. Use the [Security Profiles Operator](https://github.com/kubernetes-sigs/security-profiles-operator), SSH-based pre-loading scripts, or DaemonSets. Because the scheduler is not profile-aware, **every profile must be pre-loaded on every node** (or use node labels + `nodeSelector` to route Pods to compatible nodes only).

## API (v1.30+)

AppArmor is configured via `securityContext.appArmorProfile` at the Pod or container level. Container-level takes precedence over Pod-level.

```yaml
securityContext:
  appArmorProfile:
    type: Localhost          # RuntimeDefault | Localhost | Unconfined
    localhostProfile: k8s-apparmor-example-deny-write  # only for Localhost type
```

- **`RuntimeDefault`**: the container runtime's built-in default profile
- **`Localhost`**: a named profile pre-loaded on the node; `localhostProfile` is required
- **`Unconfined`**: no AppArmor enforcement (default if field is absent)

> ⚠️ Prior to v1.30 AppArmor was specified via annotations. The annotation API is deprecated — use `securityContext` instead.

## Key Commands

```bash
# Check AppArmor is enabled on a node
cat /sys/module/apparmor/parameters/enabled    # Y = enabled

# See loaded profiles on a node (via SSH)
sudo cat /sys/kernel/security/apparmor/profiles | sort

# Load a profile onto nodes (example using SSH)
NODES=($(kubectl get node -o jsonpath='{.items[*].status.addresses[?(.type=="Hostname")].address}'))
for NODE in ${NODES[*]}; do
  ssh $NODE 'sudo apparmor_parser -q <<EOF
#include <tunables/global>
profile k8s-apparmor-example-deny-write flags=(attach_disconnected) {
  #include <abstractions/base>
  file,
  deny /** w,   # deny all writes
}
EOF'
done

# Deploy a Pod with the deny-write profile
kubectl create -f hello-apparmor.yaml

# Verify the profile is applied
kubectl exec hello-apparmor -- cat /proc/1/attr/current
# Expected: k8s-apparmor-example-deny-write (enforce)

# Trigger a violation — write should fail
kubectl exec hello-apparmor -- touch /tmp/test
# Error: touch: /tmp/test: Permission denied

# Try to create a Pod referencing a missing profile → stays Pending
kubectl describe pod hello-apparmor-2
# Events: Warning Failed — apparmor profile not found k8s-apparmor-example-allow-write
```

## Prerequisites

- Linux nodes with AppArmor kernel module enabled
- Kubernetes v1.31+ (earlier versions supported via annotations, deprecated)
- Profiles pre-loaded on all target nodes before Pod creation

## Key Concepts

- **AppArmor profile**: a text file defining the MAC policy for a process; loaded into the kernel with `apparmor_parser`; enforced transparently at kernel level
- **`type: Localhost`**: the only type that allows custom profiles; requires `localhostProfile` name matching a loaded profile
- **Missing profile → Pod stuck Pending**: the kubelet rejects Pod admission if the requested profile isn't loaded; visible as `Warning Failed` event
- **Violation → Permission denied**: the kernel silently blocks the denied operation; `dmesg` and `journalctl` show detailed audit messages
- **Profile authoring tools**: `aa-genprof`/`aa-logprof` monitor app activity and suggest rules; `bane` provides a simplified profile language
- **Scope**: Pod-level sets the default for all containers (including init, sidecar, ephemeral); container-level overrides Pod-level

## Cross-references

- [[seccomp]] — complementary syscall-level restriction (AppArmor = MAC policy, seccomp = syscall filter)
- [[ns-level-pss]] — Pod Security Standards can enforce `RuntimeDefault` AppArmor via `restricted` level
- [[pod-sidecar-containers]] — AppArmor applies independently to sidecar containers
- [[kubernetes-topic-taxonomy]] — `apparmor`, `security-context`, `linux`, `kernel` domains

## Sources

- `docs/wiki/raw/tutorials/apparmor.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/security/apparmor/
