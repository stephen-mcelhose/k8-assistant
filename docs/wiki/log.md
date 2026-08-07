# Wiki Log

<!-- Append-only. Never edit existing entries. -->

## [2026-08-07] init | wiki initialized at docs/wiki/
## [2026-08-07] ingest | docs/pr-notes.md — PR #16 original analysis
## [2026-08-07] ingest | Deploy an App (Tutorial #2) — https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/
## [2026-08-07] ingest | Explore Your App (Tutorial #3) — https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/
## [2026-08-07] lint | 8 pages checked, 1 issue found, 1 fixed (missing cross-refs in kubernetes-topic-taxonomy.md); 4 forward-ref advisories noted (expose-app, scale-app, namespaces-walkthrough, expose-external-ip — pending ingest)
## [2026-08-07] ingest | Scale Up Your App (Tutorial #5) — https://kubernetes.io/docs/tutorials/kubernetes-basics/scale/scale-intro/
## [2026-08-07] lint | 9 pages checked, 0 issues, 0 fixed; [[scale-app]] forward-ref resolved; 4 forward-ref advisories remain (expose-app 5×, update-app 2×, namespaces-walkthrough 1×, expose-external-ip 1× — all Batch 2)
## [2026-08-07] process | raw/ backfilled with verbatim extractions (deploy-app, explore-app, scale-app); extract.py + LICENSE-raw.md added; AGENTS.md updated with new ingest workflow; .gitattributes added
## [2026-08-07] ingest | expose-external-ip (#14, score 3.2) — LoadBalancer Service on cloud providers; propagated kubernetes-topic-taxonomy
## [2026-08-07] ingest | batch 2 complete — namespaces-walkthrough (#23), expose-app (#4), update-app (#6), configure-redis-configmap (#8), guestbook (#15), connect-applications-service (#24); forward-refs [[expose-app]] and [[update-app]] resolved; taxonomy + index updated
## [2026-08-07] ingest | batch 3 complete — ns-level-pss (#11), updating-configuration-via-a-configmap (#7), pod-sidecar-containers (#9), basic-stateful-set (#16), cassandra (#18); taxonomy + index updated
## [2026-08-07] ingest | batch 4 complete — create-cluster (#1), mysql-wordpress-persistent-volume (#17), pods-and-endpoint-termination-flow (#26), source-ip (#25); taxonomy + index updated
## [2026-08-07] ingest | batch 5 complete — apparmor (#12), seccomp (#13), provision-swap-memory (#21), zookeeper (#19); taxonomy + index updated
## [2026-08-07] ingest | batch 6 complete — cluster-level-pss (#10), kubelet-standalone (#20), install-use-dra (#22); taxonomy + index updated; ALL 26 tutorials ingested
## [2026-08-07] ingest | kubectl-quick-reference (kubernetes.io reference page); manual tag-taxonomy.md raw ingested; taxonomy Application Examples + Testing & Utilities sections added; broken resource ref fixed
