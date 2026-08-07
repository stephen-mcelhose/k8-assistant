---
type: concept
title: Running Kubelet in Standalone Mode
description: How to run kubelet without a control plane — installing CRI-O and CNI plugins on a bare Linux host, configuring kubelet with staticPodPath, and managing Pods purely via manifest files dropped into a watched directory.
resource: https://kubernetes.io/docs/tutorials/cluster-management/kubelet-standalone/
tags: [kubelet, standalone, cri-o, cni, static-pod, systemd, linux, container-runtime]
timestamp: 2026-08-07T00:00:00Z
---

# Running Kubelet in Standalone Mode

Standalone mode runs the kubelet as a Linux daemon directly on a host, **with no Kubernetes API server**. The kubelet manages containers locally using static Pod manifests from a watched directory. There is no scheduler, no controller manager, no etcd — just kubelet + container runtime + CNI.

**When is this useful?**
- Learning Kubernetes node mechanics without a full cluster
- Running the Kubernetes control plane itself as static Pods (kubeadm bootstraps this way)
- Edge or embedded scenarios where a full control plane is impractical

The key config difference from a normal kubelet: the `--kubeconfig` flag is **omitted**. Without it, kubelet cannot connect to an API server and enters standalone mode. Pods are created by dropping YAML files into `staticPodPath`.

## Setup steps

**1. System prerequisites**
```bash
# Disable swap (or set failSwapOn: false in kubelet config)
sudo swapoff -a

# Enable IPv4 packet forwarding
sudo tee /etc/sysctl.d/k8s.conf <<EOF
net.ipv4.ip_forward = 1
EOF
sudo sysctl --system
```

**2. Install CRI-O** (the container runtime)
```bash
# Static binary bundle — installs CRI-O + cni-plugins + crun/runc
curl https://raw.githubusercontent.com/cri-o/packaging/main/get > crio-install
sudo bash crio-install
sudo systemctl daemon-reload
sudo systemctl enable --now crio.service
sudo systemctl is-active crio.service   # → active
```

**3. Install and configure kubelet**
```bash
# Download kubelet binary
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubelet"
chmod +x kubelet && sudo cp kubelet /usr/bin/

# Create static pod directory and kubelet config
sudo mkdir -p /etc/kubernetes/manifests
sudo tee /etc/kubernetes/kubelet.yaml <<EOF
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
authentication:
  webhook:
    enabled: false     # insecure — tutorial only
authorization:
  mode: AlwaysAllow    # insecure — tutorial only
enableServer: false
logging:
  format: text
address: 127.0.0.1
readOnlyPort: 10255    # insecure — tutorial only
staticPodPath: /etc/kubernetes/manifests
containerRuntimeEndpoint: unix:///var/run/crio/crio.sock
EOF

# Create systemd unit (no --kubeconfig = standalone mode)
sudo tee /etc/systemd/system/kubelet.service <<EOF
[Unit]
Description=Kubelet
[Service]
ExecStart=/usr/bin/kubelet --config=/etc/kubernetes/kubelet.yaml
Restart=always
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now kubelet.service
```

**4. Run a static Pod**
```bash
# Drop a Pod manifest into the watched directory
cat <<EOF | sudo tee /etc/kubernetes/manifests/static-web.yaml
apiVersion: v1
kind: Pod
metadata:
  name: static-web
spec:
  containers:
  - name: web
    image: nginx
    ports:
    - name: web
      containerPort: 80
      protocol: TCP
EOF

# Kubelet detects the file and starts the container automatically
curl http://localhost:10255/pods | jq '.items[].status.podIP'
curl http://<podIP>    # nginx welcome page
```

## Key Commands

```bash
# Check kubelet health via its local API
curl http://localhost:10255/healthz?verbose
curl http://localhost:10255/pods | jq '.'

# Verify CRI-O is running
sudo systemctl is-active crio.service
sudo journalctl -f -u crio.service

# Verify CNI bridge plugin
/opt/cni/bin/bridge --version
cat /etc/cni/net.d/11-crio-ipv4-bridge.conflist

# Remove a static Pod: delete the manifest file
sudo rm /etc/kubernetes/manifests/static-web.yaml
# Kubelet notices the file is gone and terminates the container

# Full cleanup
sudo systemctl disable --now kubelet.service crio.service
sudo rm /etc/systemd/system/kubelet.service /usr/bin/kubelet
sudo rm -rf /etc/kubernetes /var/lib/kubelet /var/log/containers /var/log/pods
sudo rm -rf /usr/local/bin /usr/local/lib /usr/local/share /usr/libexec/crio
sudo rm -rf /etc/crio /etc/containers /opt/cni /etc/cni /var/lib/cni
```

## Prerequisites

- A Linux host with systemd and iptables (or nftables with iptables emulation)
- Root access
- Internet access (to download CRI-O, kubelet, nginx image)
- Tools: `curl`, `tar`, `jq`
- No swap, or `failSwapOn: false` in kubelet config

## Key Concepts

- **Standalone mode**: kubelet without `--kubeconfig`; no API server, scheduler, or controller manager; Pods managed purely via static manifests
- **Static Pod**: a Pod manifest file in `staticPodPath`; kubelet watches the directory and creates/deletes containers as files appear/disappear; not managed by any controller
- **`staticPodPath`**: the directory kubelet watches for Pod manifests; default `/etc/kubernetes/manifests`; adding or removing files is the sole Pod management API in standalone mode
- **CRI-O + CNI**: CRI-O is the container runtime (implements CRI); cni-plugins provides the bridge networking; together they give containers a network interface and Pod-to-Pod connectivity
- **`readOnlyPort: 10255`**: kubelet's unauthenticated read-only HTTP API; fine for local debugging, never expose in production
- **No ConfigMap/Secret support**: in standalone mode, containers cannot reference ConfigMaps or Secrets — those require a control plane; use env vars in the manifest directly
- **`containerRuntimeEndpoint`**: the Unix socket path to the CRI implementation; for CRI-O: `unix:///var/run/crio/crio.sock`

## Cross-references

- [[create-cluster]] — minikube gives a full cluster with control plane; the counterpart to standalone mode
- [[provision-swap-memory]] — swap configuration on Linux nodes; relevant to the `failSwapOn` requirement
- [[explore-app]] — `kubectl logs` and `kubectl describe` — the equivalent operations in standalone mode use the kubelet API directly
- [[kubernetes-topic-taxonomy]] — `kubelet`, `standalone`, `cri-o`, `cni`, `static-pod` domains

## Sources

- `docs/wiki/raw/tutorials/kubelet-standalone.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/cluster-management/kubelet-standalone/
