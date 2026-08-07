# Wiki Index

| Page                                                      | Summary                                                              | Tags                                      |
|-----------------------------------------------------------|----------------------------------------------------------------------|-------------------------------------------|
| [[kubernetes-topic-taxonomy]]                             | Canonical two-level tag vocabulary (~200 concepts across 25 domains) | taxonomy, kubectl, kubernetes, indexing   |
| [[learning-aid-rubric]]                                   | 6-criterion pedagogical scoring framework for evaluating the skill   | pedagogy, evaluation, learning            |
| [[tutorial-coverage-scoring]]                             | Context score formula and tutorial sequencing rationale              | tutorials, scoring, pedagogy              |
| [[security-considerations]]                               | Known security surface of the skill (SQP-2, credential exposure)    | security, kubectl, credentials            |
| [[skill-design-principles]]                               | Design intent: novel environment framing, discover-then-guide        | skill-design, pedagogy, architecture      |
| [[tutorial-sync-plan]]                                    | Plan for ingesting all 26 kubernetes.io tutorials into the wiki      | tutorials, sync, maintenance              |
| [[deploy-app]]                                            | Deploy a containerised app with kubectl create deployment; access via kubectl proxy | deployment, kubectl, proxy, basics |
| [[explore-app]]                                           | Inspect Pods and Nodes with kubectl describe, logs, and exec — core debugging toolkit | pod, node, describe, exec, debug  |
| [[scale-app]]                                             | Scale a Deployment up/down with kubectl scale; ReplicaSets and Service load balancing | scale, replicaset, replicas, load-balancing |
| [[expose-external-ip]]                                    | Expose a Deployment via LoadBalancer Service on a cloud provider; verify endpoints and clean up | service, loadbalancer, external-ip, cloud |
| [[namespaces-walkthrough]]                                | Partition a cluster with namespaces; create per-namespace kubectl contexts and switch between them | namespace, context, use-context           |
| [[expose-app]]                                            | Expose a Deployment with NodePort Service; labels/selectors; Service types overview              | service, nodeport, selector, labels       |
| [[update-app]]                                            | Rolling updates with kubectl set image; verify with rollout status; roll back with rollout undo  | rollout, rollback, rolling-update         |
| [[configure-redis-configmap]]                             | Mount a ConfigMap as a volume file; why Pod restart is required for config changes to take effect | configmap, volume, exec, configuration   |
| [[guestbook]]                                             | Multi-tier app: Redis leader/followers + PHP frontend using DNS discovery and port-forward        | port-forward, redis, multi-tier, dns      |
| [[connect-applications-service]]                          | Service networking deep dive: ClusterIP, EndpointSlices, env var vs DNS discovery, TLS, LoadBalancer | service, dns, coredns, tls, secret    |
| [[ns-level-pss]]                                          | Enforce/warn/audit Pod Security Standards per namespace via labels; baseline vs restricted levels     | pod-security, namespace, pss, kind    |
| [[updating-configuration-via-a-configmap]]                | Four ConfigMap update patterns: volume (auto), env var (rollout required), multi-container, immutable | configmap, rollout, sidecar, immutable |
| [[pod-sidecar-containers]]                                | Native sidecar containers (initContainer + restartPolicy:Always); adoption guide and webhook pitfalls | sidecar, init-containers, jobs        |
| [[basic-stateful-set]]                                    | StatefulSet full lifecycle: stable identity, ordered ops, PVC persistence, partitioned rolling update | statefulset, pvc, headless-service    |
| [[cassandra]]                                             | 3-node Cassandra ring via StatefulSet; custom seed provider; nodetool validation; PVC cleanup         | cassandra, statefulset, distributed   |
| [[create-cluster]]                                        | Kubernetes cluster model: control plane vs nodes, kubelet, minikube start                             | cluster, minikube, control-plane, node |
| [[mysql-wordpress-persistent-volume]]                     | WordPress+MySQL via Kustomize; Secret generator; Recreate strategy; PVCs; kubectl apply -k            | kustomize, pvc, secret, wordpress      |
| [[pods-and-endpoint-termination-flow]]                    | Pod termination + EndpointSlice conditions (ready/serving/terminating); connection draining            | termination, endpointslice, prestop    |
| [[source-ip]]                                             | Source IP NAT behaviour per Service type; externalTrafficPolicy:Local; healthCheckNodePort            | source-ip, nat, kube-proxy, nodeport   |
| [[apparmor]]                                              | Load AppArmor profiles onto nodes; securityContext.appArmorProfile; violation and missing-profile behavior | apparmor, security-context, linux  |
| [[seccomp]]                                               | seccomp profiles via kind extraMounts; audit→violation→fine-grained progression; RuntimeDefault default | seccomp, syscall, kind, linux         |
| [[provision-swap-memory]]                                 | Encrypted/unencrypted swap on Linux nodes; kubelet LimitedSwap config; boot persistence via systemd   | swap, kubelet, kubeadm, memory        |
| [[zookeeper]]                                             | 3-node ZooKeeper ensemble; PodAntiAffinity + PDB for quorum safety; liveness probes; cordon/drain     | zookeeper, pdb, podantiaffinity       |
| [[cluster-level-pss]]                                     | Cluster-wide PSS via AdmissionConfiguration; kube-system exemption; dry-run assessment; kind          | pod-security, cluster-level, kubeadm  |
| [[kubelet-standalone]]                                    | Kubelet without control plane; CRI-O + CNI install; staticPodPath; local kubelet API                  | kubelet, standalone, static-pod, cni  |
| [[install-use-dra]]                                       | DRA stable v1.35; DeviceClass + ResourceClaim + CEL; driver DaemonSet; allocate/deallocate lifecycle  | dra, deviceclass, resourceclaim, cel  |
