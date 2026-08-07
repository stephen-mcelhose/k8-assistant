# kubectl Quick Reference

## Command Syntax
```bash
kubectl [command] [TYPE] [NAME] [flags]
```

- **command**: Operation (get, describe, logs, etc.)
- **TYPE**: Resource type (pod, service, deployment, etc.)
- **NAME**: Resource name
- **flags**: Optional flags (--namespace, -o, etc.)

## Read-Only Operations

### Configuration & Context
```bash
kubectl config current-context                         # Show current context
kubectl config get-contexts                            # List all contexts
kubectl config view                                    # View configuration
```

### Viewing Resources
```bash
kubectl get <type>                                     # List resources
kubectl get <type> -n <namespace>                      # List in namespace
kubectl get <type> <name> -o yaml                      # Get resource YAML
kubectl describe <type> <name>                         # Detailed info
kubectl logs <pod>                                     # View logs
```

### Diagnostic Commands
```bash
kubectl cluster-info                                   # Cluster status
kubectl top nodes                                      # Node metrics
kubectl top pods                                       # Pod metrics
kubectl explain <type>                                 # Resource documentation
kubectl auth can-i <verb> <resource>                   # Check permissions
```

## Common Resource Types

| Full Name    | Short  | Description  |
|--------------|--------|--------------|
| pods         | po     | Pod          |
| services     | svc    | Service      |
| deployments  | deploy | Deployment   |
| configmaps   | cm     | ConfigMap    |
| secrets      |        | Secret       |
| namespaces   | ns     | Namespace    |
| nodes        | no     | Node         |
