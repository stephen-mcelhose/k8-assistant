# Tutorial Map

| Module | Tutorial | Quick Ref Coverage | Tutorial Quality | Task Difficulty | Context Score | Tags |
|--------|----------|--------------------|------------------|-----------------|---------------|------|
| [1](https://kubernetes.io/docs/tutorials/kubernetes-basics/create-cluster/cluster-intro/) | Create a Kubernetes Cluster | 3 | 4 | 2 | 1.9 | cluster, minikube, cluster-info, context, configuration, kubectl |
| [2](https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/) | Deploy an App | 5 | 5 | 2 | 4.0 | deployment, create, get, proxy, apply, kubectl |
| [3](https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/) | Explore Your App | 5 | 5 | 2 | 4.0 | pod, describe, logs, exec, troubleshooting, debug, kubectl |
| [4](https://kubernetes.io/docs/tutorials/kubernetes-basics/expose/expose-intro/) | Expose Your App Publicly | 5 | 5 | 3 | 3.0 | service, expose, label, selector, networking, nodeport |
| [5](https://kubernetes.io/docs/tutorials/kubernetes-basics/scale/scale-intro/) | Scale Up Your App | 5 | 5 | 2 | 4.0 | scale, replicas, replicaset, load-balancing, autoscale |
| [6](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/) | Update Your App | 5 | 5 | 3 | 3.0 | rollout, update, image, rollback, revision, set |
| [7](https://kubernetes.io/docs/tutorials/configuration/updating-configuration-via-a-configmap/) | Updating Configuration via ConfigMap | 5 | 5 | 4 | 2.0 | configmap, edit, apply, rollout, volume, environment |
| [8](https://kubernetes.io/docs/tutorials/configuration/configure-redis-using-configmap/) | Configuring Redis using ConfigMap | 5 | 4 | 3 | 3.0 | configmap, pod, volume, exec, apply, delete |
| [9](https://kubernetes.io/docs/tutorials/configuration/pod-sidecar-containers/) | Adopting Sidecar Containers | 4 | 4 | 4 | 2.0 | sidecar, pod, deployment, init-containers, describe, feature-gate |
| [10](https://kubernetes.io/docs/tutorials/security/cluster-level-pss/) | Apply Pod Security Standards at Cluster Level | 4 | 5 | 5 | 0.8 | pod-security, kind, admission-controller, baseline, restricted, privileged, dry-run, label |
| [11](https://kubernetes.io/docs/tutorials/security/ns-level-pss/) | Apply Pod Security Standards at Namespace Level | 4 | 5 | 3 | 2.4 | pod-security, namespace, label, baseline, restricted, enforce, warn, audit |
| [12](https://kubernetes.io/docs/tutorials/security/apparmor/) | Restrict Container Access with AppArmor | 3 | 4 | 5 | 1.2 | apparmor, security-context, profile, localhost, exec, ssh |
| [13](https://kubernetes.io/docs/tutorials/security/seccomp/) | Restrict Container Syscalls with seccomp | 3 | 5 | 5 | 1.2 | seccomp, security-context, syscall, kind, localhost, runtime-default |
| [14](https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/) | Exposing External IP Address | 5 | 4 | 2 | 3.2 | loadbalancer, expose, external-ip, curl, replicaset |
| [15](https://kubernetes.io/docs/tutorials/stateless-application/guestbook/) | Deploying PHP Guestbook with Redis | 5 | 5 | 3 | 3.0 | guestbook, frontend, backend, tier, role, follower, leader, port-forward |
| [16](https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/) | StatefulSet Basics | 5 | 5 | 4 | 2.0 | statefulset, ordinal, headless-service, volumeclaimtemplate, pvc, pv, scale, patch, rolling-update, partition |
| [17](https://kubernetes.io/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/) | WordPress and MySQL with Persistent Volumes | 4 | 4 | 3 | 1.9 | wordpress, mysql, kustomize, secret, deployment, persistentvolume, storageclass |
| [18](https://kubernetes.io/docs/tutorials/stateful-application/cassandra/) | Deploying Cassandra with StatefulSet | 5 | 4 | 4 | 2.0 | cassandra, statefulset, headless-service, nodetool, seed, ring, edit |
| [19](https://kubernetes.io/docs/tutorials/stateful-application/zookeeper/) | Running ZooKeeper | 5 | 5 | 5 | 1.0 | zookeeper, statefulset, poddisruptionbudget, podantiaffinity, quorum, ensemble, cordon, drain, uncordon |
| [20](https://kubernetes.io/docs/tutorials/cluster-management/kubelet-standalone/) | Running Kubelet in Standalone Mode | 2 | 4 | 5 | 0.8 | kubelet, standalone, cri-o, crio, systemd, static-pod, container-runtime, cni, network-plugin, swap, swapon, swapoff, sysctl, crun, runc, crictl, journalctl |
| [21](https://kubernetes.io/docs/tutorials/cluster-management/provision-swap-memory/) | Configuring Swap Memory on Kubernetes Nodes | 3 | 4 | 4 | 1.2 | swap, kubelet, kubeadm, fallocate, mkswap, swapon, cryptsetup, systemctl, swapbehavior, limitedswap, failswapon |
| [22](https://kubernetes.io/docs/tutorials/cluster-management/install-use-dra/) | Install Drivers and Allocate Devices with DRA | 4 | 5 | 5 | 0.8 | dra, dynamic-resource-allocation, deviceclass, resourceslice, resourceclaim, resourceclaimtemplate, daemonset, device-plugin, cdi, cel, rbac, serviceaccount, clusterrole, clusterrolebinding, priorityclass |
| [23](https://kubernetes.io/docs/tutorials/cluster-management/namespaces-walkthrough/) | Namespaces Walkthrough | 5 | 4 | 2 | 3.2 | namespace, context, config, use-context, set-context, current-context, label |
| [24](https://kubernetes.io/docs/tutorials/services/connect-applications-service/) | Connecting Applications with Services | 5 | 5 | 3 | 3.0 | service, clusterip, expose, deployment, endpoint, endpointslice, dns, coredns, nslookup, environment-variables, secret, tls, openssl, targetport, nodeport, loadbalancer, external-ip |
| [25](https://kubernetes.io/docs/tutorials/services/source-ip/) | Using Source IP | 4 | 5 | 4 | 1.6 | source-ip, nat, snat, dnat, vip, kube-proxy, iptables, externaltrafficpolicy, healthchecknodeport, wget, clusterip, nodeport, loadbalancer |
| [26](https://kubernetes.io/docs/tutorials/services/pods-and-endpoint-termination-flow/) | Explore Termination Behavior for Pods and Endpoints | 4 | 4 | 3 | 1.9 | termination, graceful-shutdown, terminationgraceperiodseconds, prestop, lifecycle, endpointslice, endpoint-conditions, serving, ready, connection-draining |


## Contextual Scoring

**Context Score Formula**: `(Quick Ref Coverage × Tutorial Quality × (6 - Task Difficulty)) / 25`

This score represents the likelihood of successfully completing the tutorial given the quick-ref guide as pre-existing context. Higher scores indicate better alignment between available context and tutorial requirements.
