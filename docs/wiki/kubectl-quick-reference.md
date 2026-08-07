---
type: reference
title: kubectl Quick Reference
description: The official kubernetes.io kubectl cheat sheet — autocomplete, context/kubeconfig, create/apply, get/describe/sort/filter/jsonpath, rollout, patch, scale, delete, logs/exec/debug/port-forward/cp, cordon/drain/taint, output formats, and verbosity levels.
resource: https://kubernetes.io/docs/reference/kubectl/quick-reference/
tags: [kubectl, reference, autocomplete, context, kubeconfig, jsonpath, output-format, patch, rollout, debug, cordon, drain, taint, verbosity]
timestamp: 2026-08-07T00:00:00Z
---

# kubectl Quick Reference

The canonical kubectl command reference from kubernetes.io. This page is the companion to the wiki tutorials — use it to look up exact flags and syntax while working through any tutorial.

## Autocomplete

```bash
# Bash
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
alias k=kubectl
complete -o default -F __start_kubectl k

# Zsh
source <(kubectl completion zsh)
echo '[[ $commands[kubectl] ]] && source <(kubectl completion zsh)' >> ~/.zshrc

# Fish (v1.23+)
echo 'kubectl completion fish | source' > ~/.config/fish/completions/kubectl.fish && source ~/.config/fish/completions/kubectl.fish
```

## Context & Configuration

```bash
kubectl config view                                        # show merged kubeconfig
kubectl config view --raw                                  # include raw cert data
kubectl config get-contexts                                # list all contexts
kubectl config get-contexts -o name                        # names only
kubectl config current-context                             # show active context
kubectl config use-context my-cluster-name                 # switch context
kubectl config set-context --current --namespace=mynamespace  # set default namespace
kubectl config set-context gce --user=cluster-admin --namespace=foo && kubectl config use-context gce
kubectl config unset users.foo                             # delete a user

# Handy aliases (bash/zsh)
alias kx='f() { [ "$1" ] && kubectl config use-context $1 || kubectl config current-context ; } ; f'
alias kn='f() { [ "$1" ] && kubectl config set-context --current --namespace $1 || kubectl config view --minify | grep namespace | cut -d" " -f6 ; } ; f'

# --all-namespaces shorthand
kubectl -A get pods
```

## Creating Objects

```bash
kubectl apply -f ./my-manifest.yaml               # create/update from file
kubectl apply -f ./my1.yaml -f ./my2.yaml          # multiple files
kubectl apply -f ./dir                             # all manifests in directory
kubectl apply -f https://example.com/manifest.yaml # from URL

kubectl create deployment nginx --image=nginx
kubectl create job hello --image=busybox:1.28 -- echo "Hello World"
kubectl create cronjob hello --image=busybox:1.28 --schedule="*/1 * * * *" -- echo "Hello World"
kubectl explain pods                               # API field documentation
```

## Viewing & Finding Resources

```bash
# Basic get
kubectl get services
kubectl get pods --all-namespaces                  # or: kubectl get pods -A
kubectl get pods -o wide
kubectl get pod my-pod -o yaml
kubectl describe nodes my-node
kubectl describe pods my-pod

# Sorting
kubectl get services --sort-by=.metadata.name
kubectl get pods --sort-by='.status.containerStatuses[0].restartCount'
kubectl get pv --sort-by=.spec.capacity.storage

# Label / field selectors
kubectl get pods --selector=app=cassandra -o jsonpath='{.items[*].metadata.labels.version}'
kubectl get pods --field-selector=status.phase=Running
kubectl get node --selector='!node-role.kubernetes.io/control-plane'

# JSONPath
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'
kubectl get secret my-secret -o go-template='{{range $k,$v := .data}}{{"### "}}{{$k}}{{"\n"}}{{$v|base64decode}}{{"\n\n"}}{{end}}'
kubectl get configmap myconfig -o jsonpath='{.data.ca\.crt}'

# custom-columns
kubectl get node -o custom-columns='NODE_NAME:.metadata.name,STATUS:.status.conditions[?(@.type=="Ready")].status'

# Other
kubectl get pods --show-labels
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl events --types=Warning
kubectl diff -f ./my-manifest.yaml
kubectl get deployment nginx-deployment --subresource=status

# Explore JSON key paths with jq
kubectl get nodes -o json | jq -c 'paths|join(".")'
```

## Updating Resources

```bash
kubectl set image deployment/frontend www=image:v2      # rolling update image
kubectl rollout history deployment/frontend             # view revision history
kubectl rollout undo deployment/frontend                # rollback to previous
kubectl rollout undo deployment/frontend --to-revision=2
kubectl rollout status -w deployment/frontend           # watch until complete
kubectl rollout restart deployment/frontend             # rolling restart

kubectl label pods my-pod new-label=awesome
kubectl label pods my-pod new-label-                    # remove label
kubectl label pods my-pod new-label=new-value --overwrite
kubectl annotate pods my-pod icon-url=http://goo.gl/XXBTWq
kubectl annotate pods my-pod icon-url-                  # remove annotation
kubectl autoscale deployment foo --min=2 --max=10
```

## Patching Resources

```bash
# Strategic merge patch
kubectl patch node k8s-node-1 -p '{"spec":{"unschedulable":true}}'
kubectl patch pod valid-pod -p '{"spec":{"containers":[{"name":"kubernetes-serve-hostname","image":"new image"}]}}'

# JSON patch (positional arrays)
kubectl patch pod valid-pod --type='json' -p='[{"op":"replace","path":"/spec/containers/0/image","value":"new image"}]'
kubectl patch deployment valid-deployment --type json -p='[{"op":"remove","path":"/spec/template/spec/containers/0/livenessProbe"}]'

# Scale via subresource patch
kubectl patch deployment nginx-deployment --subresource='scale' --type='merge' -p '{"spec":{"replicas":2}}'
```

## Scaling Resources

```bash
kubectl scale --replicas=3 rs/foo
kubectl scale --replicas=3 -f foo.yaml
kubectl scale --current-replicas=2 --replicas=3 deployment/mysql   # conditional scale
kubectl scale --replicas=5 rc/foo rc/bar rc/baz                    # multiple at once
```

## Deleting Resources

```bash
kubectl delete -f ./pod.json
kubectl delete pod unwanted --now                      # no grace period
kubectl delete pod,service baz foo
kubectl delete pods,services -l name=myLabel
kubectl -n my-ns delete pod,svc --all
kubectl get pods -n mynamespace --no-headers=true | awk '/pattern1|pattern2/{print $1}' | xargs kubectl delete -n mynamespace pod
```

## Interacting with Pods

```bash
# Logs
kubectl logs my-pod
kubectl logs my-pod -c my-container
kubectl logs -f my-pod                                 # stream
kubectl logs -f -l name=myLabel --all-containers
kubectl logs my-pod --previous                         # previous container instance

# Exec & shell
kubectl exec my-pod -- ls /
kubectl exec --stdin --tty my-pod -- /bin/sh
kubectl exec my-pod -c my-container -- ls /

# Debug
kubectl debug my-pod -it --image=busybox:1.28          # ephemeral container in pod
kubectl debug node/my-node -it --image=busybox:1.28    # debug on node

# Port forward & attach
kubectl port-forward my-pod 5000:6000
kubectl attach my-pod -i

# Run one-off pods
kubectl run -i --tty busybox --image=busybox:1.28 -- sh
kubectl run nginx --image=nginx --dry-run=client -o yaml > pod.yaml

# Metrics
kubectl top pod
kubectl top pod POD_NAME --containers
kubectl top pod POD_NAME --sort-by=cpu

# Copy files (requires tar in container)
kubectl cp /tmp/foo_dir my-pod:/tmp/bar_dir
kubectl cp /tmp/foo my-pod:/tmp/bar -c my-container
kubectl cp my-namespace/my-pod:/tmp/foo /tmp/bar        # remote → local
```

## Interacting with Deployments & Services

```bash
kubectl logs deploy/my-deployment
kubectl logs deploy/my-deployment -c my-container
kubectl port-forward svc/my-service 5000
kubectl port-forward svc/my-service 5000:my-service-port
kubectl port-forward deploy/my-deployment 5000:6000
kubectl exec deploy/my-deployment -- ls
```

## Interacting with Nodes & Cluster

```bash
kubectl cordon my-node                                 # mark unschedulable
kubectl drain my-node                                  # drain for maintenance
kubectl uncordon my-node                               # restore scheduling
kubectl top node
kubectl top node my-node
kubectl cluster-info
kubectl cluster-info dump
kubectl cluster-info dump --output-directory=/path/to/cluster-state
kubectl taint nodes foo dedicated=special-user:NoSchedule

# View taints via custom-columns
kubectl get nodes -o='custom-columns=NodeName:.metadata.name,TaintKey:.spec.taints[*].key,TaintValue:.spec.taints[*].value,TaintEffect:.spec.taints[*].effect'
```

## Resource Types

```bash
kubectl api-resources                                  # list all with shortnames, group, scope
kubectl api-resources --namespaced=true
kubectl api-resources --namespaced=false
kubectl api-resources -o name
kubectl api-resources -o wide
kubectl api-resources --verbs=list,get
kubectl api-resources --api-group=extensions
```

## Output Formats (`-o`)

| Flag | Description |
|------|-------------|
| `-o=custom-columns=<spec>` | Table with comma-separated custom columns |
| `-o=json`                  | Full JSON API object |
| `-o=jsonpath=<template>`   | Fields via JSONPath expression |
| `-o=go-template=<template>`| Fields via Go template |
| `-o=name`                  | Resource name only |
| `-o=wide`                  | Plain text with extra columns (node name for pods) |
| `-o=yaml`                  | Full YAML API object |
| `-o=kyaml` *(beta)*        | Kubernetes-dialect YAML |

**custom-columns examples:**
```bash
# All images in cluster
kubectl get pods -A -o=custom-columns='DATA:spec.containers[*].image'
# Images by pod in default namespace
kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,IMAGE:.spec.containers[*].image"
```

## Verbosity (`--v`)

| Flag    | Meaning |
|---------|---------|
| `--v=0` | Always visible; minimal |
| `--v=1` | Reasonable default if you don't want verbosity |
| `--v=2` | Recommended default — steady state + important messages |
| `--v=3` | Extended change information |
| `--v=4` | Debug verbosity |
| `--v=6` | Display requested resources |
| `--v=7` | Display HTTP request headers |
| `--v=8` | Display HTTP request contents |
| `--v=9` | HTTP request contents without truncation |

## Cross-references

- [[deploy-app]] — `kubectl create deployment`, `kubectl proxy`
- [[explore-app]] — `kubectl describe`, `kubectl logs`, `kubectl exec`
- [[scale-app]] — `kubectl scale`, `kubectl rollout`
- [[update-app]] — `kubectl set image`, `kubectl rollout undo`
- [[connect-applications-service]] — `kubectl expose`, `kubectl port-forward`, DNS
- [[source-ip]] — `kubectl patch svc`, `externalTrafficPolicy`
- [[zookeeper]] — `kubectl cordon`, `kubectl drain`, `kubectl taint`
- [[kubernetes-topic-taxonomy]] — tag vocabulary used across all wiki pages

## Sources

- `docs/wiki/raw/tutorials/kubectl-quick-reference.md` (verbatim extraction, CC BY 4.0)
- https://kubernetes.io/docs/reference/kubectl/quick-reference/
