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
