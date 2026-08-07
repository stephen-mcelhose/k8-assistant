---
type: concept
title: Install Drivers and Allocate Devices with DRA
description: How Dynamic Resource Allocation (DRA, stable v1.35) works — deploying a DRA driver DaemonSet, creating DeviceClasses and ResourceClaims with CEL expressions, referencing claims in Pod specs, and observing the allocate/deallocate lifecycle.
resource: https://kubernetes.io/docs/tutorials/cluster-management/install-use-dra/
tags: [dra, dynamic-resource-allocation, deviceclass, resourceclaim, resourceslice, cel, daemonset, gpu, hardware]
timestamp: 2026-08-07T00:00:00Z
---

# Install Drivers and Allocate Devices with DRA

**Dynamic Resource Allocation (DRA)** is Kubernetes' next-generation hardware device API, stable in v1.35. It replaces the limitations of the older Device Plugin framework with a structured API for expressing hardware requirements, advertising device attributes, and tracking allocation state across the Pod lifecycle.

DRA's key advance over Device Plugins: **resource claims carry structured metadata** (memory capacity, NUMA topology, etc.) that can be filtered with **CEL expressions** in the request. Users can say "give me a GPU with at least 10 GiB memory" rather than just "give me one of whatever this device class offers."

## Three-party model

| Party | Responsibility |
|-------|---------------|
| **Kubernetes built-ins** (scheduler, kubelet, kube-controller-manager) | Scheduling, binding, tracking allocation state |
| **DRA driver** (third-party DaemonSet) | Advertising devices via `ResourceSlice`, preparing/unpreparing hardware per Pod |
| **User** | Creating `ResourceClaim`/`ResourceClaimTemplate`; referencing claims in Pod specs |

## DRA API objects

| Object | Scope | Created by | Purpose |
|--------|-------|-----------|---------|
| `DeviceClass` | Cluster | Operator/driver vendor | Defines a device type; CEL selector filters which devices belong to this class |
| `ResourceSlice` | Cluster (per-node) | DRA driver | Advertises available devices on a node with their attributes |
| `ResourceClaim` | Namespace | User or controller | Requests a device; contains CEL expression for attribute requirements |
| `ResourceClaimTemplate` | Namespace | User | Creates per-Pod ResourceClaims automatically |

## Driver installation pattern

DRA drivers deploy as a **DaemonSet** with:
- RBAC: `ServiceAccount` + `ClusterRole` (`resourceslices` CRUD, `resourceclaims` get, `nodes` get) + `ClusterRoleBinding`
- **`PriorityClass`** with a high value (e.g., 1,000,000): prevents preemption of the driver Pod, which must remain running to manage device lifecycle for Pods scheduled on that node
- Volume mounts: `/var/lib/kubelet/plugins_registry` (for kubelet plugin registration), `/var/lib/kubelet/plugins` (plugin socket), `/var/run/cdi` (Container Device Interface)

## ResourceClaim with CEL

```yaml
apiVersion: resource.k8s.io/v1
kind: ResourceClaim
metadata:
  name: some-gpu
  namespace: dra-tutorial
spec:
  devices:
    requests:
    - name: some-gpu
      exactly:
        deviceClassName: gpu.example.com
        selectors:
        - cel:
            expression: "device.capacity['gpu.example.com'].memory.compareTo(quantity('10Gi')) >= 0"
```

The CEL expression uses `device.capacity['<driver>'].<attribute>` to filter device candidates by their advertised attributes.

## Pod spec integration

```yaml
spec:
  resourceClaims:
  - name: gpu                     # local name for the claim within this Pod
    resourceClaimName: some-gpu   # references the ResourceClaim object
  containers:
  - name: ctr0
    resources:
      claims:
      - name: gpu                 # allocates the "gpu" claim to this container
```

## Key Commands

```bash
# Explore initial DRA state (before any drivers)
kubectl get deviceclasses
kubectl get resourceslices
kubectl get resourceclaims -A

# --- Install example driver ---
kubectl create namespace dra-tutorial

# DeviceClass (cluster-scoped)
kubectl apply --server-side -f http://k8s.io/examples/dra/driver-install/deviceclass.yaml

# RBAC
kubectl apply --server-side -f http://k8s.io/examples/dra/driver-install/serviceaccount.yaml
kubectl apply --server-side -f http://k8s.io/examples/dra/driver-install/clusterrole.yaml
kubectl apply --server-side -f http://k8s.io/examples/dra/driver-install/clusterrolebinding.yaml

# PriorityClass (prevents driver preemption)
kubectl apply --server-side -f http://k8s.io/examples/dra/driver-install/priorityclass.yaml

# DaemonSet (the actual driver)
kubectl apply --server-side -f http://k8s.io/examples/dra/driver-install/daemonset.yaml

# Verify driver is running and advertising devices
kubectl get pod -l app.kubernetes.io/name=dra-example-driver -n dra-tutorial
kubectl get resourceslices   # one ResourceSlice per node

# --- Create a ResourceClaim and deploy a Pod ---
kubectl apply --server-side -f http://k8s.io/examples/dra/driver-install/example/resourceclaim.yaml
kubectl apply --server-side -f http://k8s.io/examples/dra/driver-install/example/pod.yaml
kubectl get pod pod0 -n dra-tutorial

# Verify allocation
kubectl get resourceclaims -n dra-tutorial            # STATE: allocated,reserved
kubectl get resourceclaim some-gpu -n dra-tutorial -o yaml  # shows which device, which node
kubectl logs pod0 -c ctr0 -n dra-tutorial | grep GPU_DEVICE  # driver-injected env var

# --- Delete Pod → observe deallocation ---
kubectl delete pod pod0 -n dra-tutorial
kubectl get resourceclaims -n dra-tutorial            # STATE: pending (available again)
kubectl logs -l app.kubernetes.io/name=dra-example-driver -n dra-tutorial  # UnprepareResourceClaims

# --- Cleanup ---
kubectl delete namespace dra-tutorial
kubectl delete deviceclass gpu.example.com
kubectl delete clusterrole dra-example-driver-role
kubectl delete clusterrolebinding dra-example-driver-role-binding
kubectl delete priorityclass dra-driver-high-priority
```

## Prerequisites

- Kubernetes v1.34+ (tutorial tested on v1.36); DRA stable in v1.35
- RBAC enabled in the cluster
- At least 2 worker nodes
- Linux nodes (tested)
- `jq` recommended for exploring API responses

## Key Concepts

- **`DeviceClass`**: the contract between the driver and Kubernetes; the scheduler uses it to identify which ResourceSlices satisfy a request
- **`ResourceSlice`**: per-node device inventory published by the driver; contains device names, attributes (memory, topology), and driver identity; updated dynamically as hardware availability changes
- **`ResourceClaim` lifecycle**: `pending` (created, not yet allocated) → `allocated,reserved` (scheduler picked a device + node) → driver calls `PrepareResourceClaims` (kubelet asks driver to prepare hardware) → `pending` (after Pod deletion, driver calls `UnprepareResourceClaims`)
- **CEL in selectors**: `device.capacity['<driver>'].<attr>`, `device.attributes['<driver>'].<attr>`, standard CEL operators; allows rich hardware selection without custom schedulers
- **PriorityClass for driver**: protects the driver DaemonSet from preemption; if the driver Pod is evicted, orphaned Pods with claims may be stuck in Terminating
- **`kubectl apply --server-side`**: used throughout; DRA objects use Server-Side Apply (SSA) for field ownership — important for driver ResourceSlice management
- **CDI (Container Device Interface)**: the standard for injecting device information into container runtimes; DRA drivers write CDI files to `/var/run/cdi`; the runtime reads them when starting containers

## Cross-references

- [[cassandra]] — comparison: StatefulSet for stateful workloads; DRA for hardware-dependent workloads
- [[zookeeper]] — PriorityClass usage for protecting critical DaemonSets (same pattern as DRA driver)
- [[namespaces-walkthrough]] — namespace isolation for DRA resources (`dra-tutorial` namespace)
- [[kubernetes-topic-taxonomy]] — `dra`, `dynamic-resource-allocation`, `deviceclass`, `resourceclaim`, `cel` domains

## Sources

- `docs/wiki/raw/tutorials/install-use-dra.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/tutorials/cluster-management/install-use-dra/
