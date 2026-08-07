---
type: concept
title: Configuring Swap Memory on Kubernetes Nodes
description: How to provision encrypted or unencrypted swap on a Linux worker node using kubeadm, enable it on boot via systemd or fstab, and configure kubelet with LimitedSwap behavior. Requires Kubernetes v1.33+.
resource: https://kubernetes.io/docs/tutorials/cluster-management/provision-swap-memory/
tags: [swap, kubelet, kubeadm, linux, memory, node, systemd]
timestamp: 2026-08-07T00:00:00Z
---

# Configuring Swap Memory on Kubernetes Nodes

Historically Kubernetes required `failSwapOn: true` — nodes with swap enabled were rejected by the kubelet. Since v1.33, swap support for worker nodes is stable and configurable. This tutorial walks through the full setup: provisioning swap storage, enabling it on boot, and telling the kubelet how to use it.

## Swap setup (two paths)

**Encrypted swap** (recommended — data at rest protected):
```bash
fallocate --length 4GiB /swapfile
chmod 600 /swapfile
cryptsetup --type plain --cipher aes-xts-plain64 --key-size 256 -d /dev/urandom open /swapfile cryptswap
mkswap /dev/mapper/cryptswap
swapon /dev/mapper/cryptswap
```

**Unencrypted swap**:
```bash
fallocate --length 4GiB /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

## Enabling swap on boot

Two options — use one, not both:

- **`/etc/fstab`**: add `/swapfile swap swap defaults 0 0` (unencrypted only; encrypted swap needs a systemd unit)
- **systemd unit**: more flexible — can delay kubelet start until swap is ready; can ensure swap stays active until kubelet and container runtime have shut down cleanly

## kubelet configuration

Two fields must be set in the kubelet config file:

```yaml
failSwapOn: false
memorySwap:
  swapBehavior: LimitedSwap
```

Then restart kubelet:
```bash
systemctl restart kubelet.service
```

**`swapBehavior` options:**
- `LimitedSwap` — Pods can use swap up to a limit determined by the kubelet; the default for swap-enabled nodes
- `NoSwap` — kubelet runs with swap present but Pods cannot use it
- `UnlimitedSwap` — no limit on Pod swap usage (experimental)

## Key Commands

```bash
# Verify swap is active
swapon -s
free -h   # Swap row should show non-zero total

# Edit kubelet config (location varies by distro/kubeadm setup)
# Typically: /var/lib/kubelet/config.yaml or /etc/kubernetes/kubelet-config.yaml
# Add: failSwapOn: false + memorySwap.swapBehavior: LimitedSwap

# Restart kubelet after config change
systemctl restart kubelet.service
systemctl status kubelet.service

# Verify kubelet is healthy
kubectl get node <node-name>
kubectl describe node <node-name>   # check Conditions
```

## Prerequisites

- Kubernetes v1.33+ (swap support is stable)
- Linux worker nodes (swap is a Linux feature; not applicable to control plane nodes)
- `kubeadm` installed on worker nodes
- For encrypted swap: `cryptsetup` installed
- Tools: `fallocate`, `mkswap`, `swapon`

## Key Concepts

- **`failSwapOn: false`**: permits the kubelet to start even when swap is detected; without this, kubelet refuses to start on a node with active swap
- **`LimitedSwap`**: the recommended production swap behavior — allows Pod swap usage within controlled limits; protects other workloads from swap exhaustion
- **Encrypted swap**: the recommended security posture for production; uses `cryptsetup plain` mode with a random key generated at each boot (key never stored to disk)
- **systemd for boot activation**: lets the OS ordering system ensure swap is available before kubelet starts; also ensures clean shutdown order (kubelet stops before swap is deactivated)
- **Scope**: swap configuration is per-node (kubelet config); cluster-wide defaults cannot be set centrally

## Cross-references

- [[create-cluster]] — node architecture; kubelet's role on each worker node
- [[namespaces-walkthrough]] — resource limits and quotas interact with swap behavior
- [[kubernetes-topic-taxonomy]] — `swap`, `kubelet`, `kubeadm`, `linux`, `memory` domains

## Sources

- `docs/wiki/raw/tutorials/provision-swap-memory.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/cluster-management/provision-swap-memory/
