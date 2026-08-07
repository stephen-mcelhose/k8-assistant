# Notes from csgdaa-skills PR #16

Source: `bayer-int/csgdaa-skills` PR #16 — "feat(x): publish k8s-assistant skill" (branch: `k8-learner`, closed/unmerged)

---

## Tags (for future indexing/discovery)

### Core kubectl
kubectl, command, syntax, alias, shortcut, reference, documentation, best-practices

### Configuration & Context
configuration, context, kubeconfig, use-context, set-context, current-context, namespace

### Basic Commands (Imperative)
create, apply, get, describe, delete, edit, patch, run, expose, explain

### Resource Management
scale, rollout, label, annotate, set, update, restart, rollback, revision, history, status

### Workload Resources
pod, deployment, replicaset, statefulset, daemonset, job, cronjob

### Configuration Resources
configmap, secret, secret-generator

### Storage Resources
volume, volume-mount, persistentvolume, persistentvolumeclaim, pvc, pv, emptydir, storageclass, volumeclaimtemplate

### Networking Resources
service, ingress, networkpolicy, endpoint, endpointslice, headless-service

### Service Types & Networking
clusterip, nodeport, loadbalancer, external-ip, targetport, dns, coredns

### Cluster Resources
node, namespace, serviceaccount, horizontalpodautoscaler, hpa, poddisruptionbudget, priorityclass

### Output Formats
output-format, yaml, json, jsonpath, wide, custom-columns

### Filtering & Selection
filtering, selector, label-selector, field-selector, sort, watch

### Debugging & Troubleshooting
debug, troubleshooting, logs, exec, port-forward, proxy, attach, events, top, metrics, resource-usage, verbosity, debugging

### Container & Pod Configuration
container, image, replicas, environment, environment-variables, init-containers, sidecar, multi-container, restartpolicy, liveness-probe, readiness-probe

### Lifecycle & Termination
lifecycle, prestop, termination, graceful-shutdown, terminationgraceperiodseconds, endpoint-conditions, serving, ready, connection-draining

### Node Management
taint, cordon, drain, uncordon

### Scaling & Load Balancing
autoscale, load-balancing, rolling-update, partition, canary

### Security - RBAC
security, rbac, authentication, authorization, clusterrole, clusterrolebinding

### Security - Pod Security
pod-security, admission-controller, baseline, restricted, privileged, enforce, warn, audit

### Security - Advanced
security-context, apparmor, seccomp, profile, syscall, runtime-default, tls, openssl

### Cluster Management
cluster, cluster-info, api-resources, api-versions, version, minikube, kubeadm, kind

### Container Runtime & Low Level
kubelet, standalone, container-runtime, cri-o, crio, crun, runc, crictl, systemd, static-pod, cni, network-plugin, journalctl

### Resource Allocation
dra, dynamic-resource-allocation, deviceclass, resourceslice, resourceclaim, resourceclaimtemplate, device-plugin, cdi, cel

### Swap Configuration
swap, swapon, swapoff, sysctl, fallocate, mkswap, cryptsetup, swapbehavior, limitedswap, failswapon

### Networking Details
networking, source-ip, nat, snat, dnat, vip, kube-proxy, iptables, externaltrafficpolicy, healthchecknodeport

### Deployment Patterns
imperative, declarative, feature-gate, immutable, dry-run, wait, kustomize

### Automation & Tooling
script, automation, plugin, completion, bash, zsh, fish

---

## Learning Aid Rubric (from PR comments)

A rubric proposed in the PR for evaluating the skill as a pedagogical tool. Scores on a 1–4 scale per criterion, weighted to a 100-point total.

| Criterion                        | Weight | 4 (Excellent)                                                       |
|----------------------------------|--------|---------------------------------------------------------------------|
| Engagement and Motivation        | 20%    | Resonates with real-world challenges, encourages active participation |
| Relevance to Audience            | 20%    | Addresses developer/novice DevOps pain points, builds practical skills |
| Ease of Understanding            | 15%    | Simple language, builds progressively, appropriate prior knowledge assumed |
| Practical Application            | 20%    | Hands-on, actionable examples immediately applicable                |
| Support for Learning Outcomes    | 15%    | Clear measurable objectives, skill improvement in troubleshooting   |
| Feedback & Assessment            | 10%    | Self-checks, progression indicators                                 |

**Score thresholds**: 90–100 Excellent · 70–89 Good · 50–69 Fair · <50 Poor

The rubric was noted as a potential composition point — either baked into the skill prompt or used as a standalone evaluation overlay.

---

## Automated Review (BayerReadOnlyBot / csgdaa-code)

**Grade: A (Security) · Approved with minor suggestions**

- `allowed-tools` granularity rated as strong least-privilege enforcement
- Suggestions (non-blocking):
  - Move `kubectl` commands into a wrapper script (e.g. `scripts/kubectl-read.sh`) for centralised flag validation
  - Consider removing `Bash(ls:*)` if `Glob` covers all discovery needs

---

## SkillSpector Security Scan

**Score: 17/100 · Severity: LOW · Recommendation: SAFE**

| ID    | Severity | Location                      | Finding                                                                                          |
|-------|----------|-------------------------------|--------------------------------------------------------------------------------------------------|
| SDI-4 | 🟢 LOW   | `SKILL.md:44–47`              | "Read-Only" label while also surfacing write commands — mislabelled restriction (now removed)    |
| SQP-2 | 🟡 MED   | `SKILL.md:9`                  | `kubectl config view` output may contain credentials; recommend warning or redaction before display |
| MP3   | 🔴 HIGH  | `references/tutorial-map.md:25` | Low-confidence (26%) memory manipulation flag on tutorial-map content — likely a false positive  |

> **SQP-2 action item**: Consider warning the user before running `kubectl config view` that output may include tokens/certs, or prefer `kubectl config current-context` / `kubectl config get-contexts` when full config inspection isn't needed.
