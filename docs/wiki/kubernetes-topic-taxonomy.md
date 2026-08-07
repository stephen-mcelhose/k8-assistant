---
type: concept
title: Kubernetes Topic Taxonomy
description: Canonical two-level tag vocabulary covering ~200 Kubernetes concepts across 25 domains, used for tutorial matching and indexing within the k8s-assistant skill.
resource: docs/pr-notes.md
tags: [taxonomy, kubectl, kubernetes, indexing, tags]
timestamp: 2026-08-07T15:39:38Z
---

# Kubernetes Topic Taxonomy

The k8s-assistant uses a structured tag vocabulary to match user questions to the right tutorials. Each tag maps to one or more entries in [[tutorial-coverage-scoring]], letting the skill score how well a tutorial covers the user's current topic.

The taxonomy has two levels: a **domain** (broad grouping) and **tags** within it. Tags are lowercase, hyphenated, and match the wording used in kubernetes.io tutorials.

## Taxonomy

### Core kubectl
`kubectl` `command` `syntax` `alias` `shortcut` `reference` `documentation` `best-practices`

### Configuration & Context
`configuration` `context` `kubeconfig` `use-context` `set-context` `current-context` `namespace`

### Basic Commands (Imperative)
`create` `apply` `get` `describe` `delete` `edit` `patch` `run` `expose` `explain`

### Resource Management
`scale` `rollout` `label` `annotate` `set` `update` `restart` `rollback` `revision` `history` `status`

### Workload Resources
`pod` `deployment` `replicaset` `statefulset` `daemonset` `job` `cronjob`

### Configuration Resources
`configmap` `secret` `secret-generator`

### Storage Resources
`volume` `volume-mount` `persistentvolume` `persistentvolumeclaim` `pvc` `pv` `emptydir` `storageclass` `volumeclaimtemplate`

### Networking Resources
`service` `ingress` `networkpolicy` `endpoint` `endpointslice` `headless-service`

### Service Types & Networking
`clusterip` `nodeport` `loadbalancer` `external-ip` `targetport` `dns` `coredns`

### Cluster Resources
`node` `namespace` `serviceaccount` `horizontalpodautoscaler` `hpa` `poddisruptionbudget` `priorityclass`

### Output Formats
`output-format` `yaml` `json` `jsonpath` `wide` `custom-columns`

### Filtering & Selection
`filtering` `selector` `label-selector` `field-selector` `sort` `watch`

### Debugging & Troubleshooting
`debug` `troubleshooting` `logs` `exec` `port-forward` `proxy` `attach` `events` `top` `metrics` `resource-usage` `verbosity`

### Container & Pod Configuration
`container` `image` `replicas` `environment` `environment-variables` `init-containers` `sidecar` `multi-container` `restartpolicy` `liveness-probe` `readiness-probe`

### Lifecycle & Termination
`lifecycle` `prestop` `termination` `graceful-shutdown` `terminationgraceperiodseconds` `endpoint-conditions` `serving` `ready` `connection-draining`

### Node Management
`taint` `cordon` `drain` `uncordon`

### Scaling & Load Balancing
`autoscale` `load-balancing` `rolling-update` `partition` `canary`

### Security — RBAC
`security` `rbac` `authentication` `authorization` `clusterrole` `clusterrolebinding`

### Security — Pod Security
`pod-security` `admission-controller` `baseline` `restricted` `privileged` `enforce` `warn` `audit`

### Security — Advanced
`security-context` `apparmor` `seccomp` `profile` `syscall` `runtime-default` `tls` `openssl`

### Cluster Management
`cluster` `cluster-info` `api-resources` `api-versions` `version` `minikube` `kubeadm` `kind`

### Container Runtime & Low Level
`kubelet` `standalone` `container-runtime` `cri-o` `crio` `crun` `runc` `crictl` `systemd` `static-pod` `cni` `network-plugin` `journalctl`

### Resource Allocation (DRA)
`dra` `dynamic-resource-allocation` `deviceclass` `resourceslice` `resourceclaim` `resourceclaimtemplate` `device-plugin` `cdi` `cel`

### Swap Configuration
`swap` `swapon` `swapoff` `sysctl` `fallocate` `mkswap` `cryptsetup` `swapbehavior` `limitedswap` `failswapon`

### Networking Details
`source-ip` `nat` `snat` `dnat` `vip` `kube-proxy` `iptables` `externaltrafficpolicy` `healthchecknodeport`

### Deployment Patterns
`imperative` `declarative` `feature-gate` `immutable` `dry-run` `wait` `kustomize`

### Automation & Tooling
`script` `automation` `plugin` `completion` `bash` `zsh` `fish`

## How it's used

When a user asks about a topic, the skill checks which tags match, then looks up those tags in `references/tutorial-map.md` (see [[tutorial-coverage-scoring]]) to find the highest-scoring tutorials to suggest. Tags also power future search/indexing if the wiki is ever queried externally.

**Concrete examples (ingested tutorials):**

| Tags | Tutorial page |
|------|--------------|
| `deployment`, `create`, `proxy`, `node` | [[deploy-app]] |
| `pod`, `node`, `describe`, `logs`, `exec`, `debug` | [[explore-app]] |
| `scale`, `replicaset`, `replicas`, `load-balancing` | [[scale-app]] |
| `service`, `loadbalancer`, `external-ip`, `expose` | [[expose-external-ip]] |
| `namespace`, `context`, `use-context`, `kubectl-config` | [[namespaces-walkthrough]] |
| `service`, `nodeport`, `selector`, `labels`, `expose` | [[expose-app]] |
| `rollout`, `rollback`, `rolling-update`, `set-image` | [[update-app]] |
| `configmap`, `volume`, `exec`, `configuration` | [[configure-redis-configmap]] |
| `port-forward`, `multi-tier`, `redis`, `dns` | [[guestbook]] |
| `service`, `dns`, `coredns`, `endpointslice`, `tls`, `secret` | [[connect-applications-service]] |
| `pod-security`, `namespace`, `pss`, `baseline`, `restricted` | [[ns-level-pss]] |
| `configmap`, `volume`, `env-var`, `rollout`, `sidecar`, `immutable` | [[updating-configuration-via-a-configmap]] |
| `sidecar`, `init-containers`, `restart-policy`, `jobs` | [[pod-sidecar-containers]] |
| `statefulset`, `pvc`, `headless-service`, `partition`, `ordered` | [[basic-stateful-set]] |
| `cassandra`, `statefulset`, `seed-provider`, `distributed` | [[cassandra]] |
| `cluster`, `minikube`, `control-plane`, `node`, `kubelet` | [[create-cluster]] |
| `kustomize`, `pvc`, `secret`, `recreate`, `wordpress`, `mysql` | [[mysql-wordpress-persistent-volume]] |
| `termination`, `graceful-shutdown`, `endpointslice`, `prestop` | [[pods-and-endpoint-termination-flow]] |
| `source-ip`, `nat`, `kube-proxy`, `external-traffic-policy` | [[source-ip]] |

## Sources

- `docs/pr-notes.md` — tag list originally authored for csgdaa-skills PR #16
- `references/tutorial-map.md` — tag column per tutorial
