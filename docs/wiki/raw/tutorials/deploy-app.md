# Using kubectl to Create a Deployment

Source: https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/
Fetched: 2026-08-07

---

## Objectives

- Learn about application Deployments.
- Deploy your first app on Kubernetes with `kubectl`.

---

## Before You Begin (Prerequisites)

- **Shell Compatibility:** POSIX shell syntax (bash, zsh, sh). Windows users need WSL or Git Bash.
- **CPU Architecture:** Tutorial uses a container requiring AMD64. On non-AMD64 machines, try `minikube` with a Docker Desktop driver.
- **Kubernetes Tools:** `kubectl` installed and a running Kubernetes cluster.

---

## Key Concepts

### Kubernetes Deployments

A Deployment is responsible for creating and updating instances of your application. Once you create a Deployment, the Kubernetes control plane schedules the application instances to run on individual Nodes. A Kubernetes Deployment controller continuously monitors those instances and replaces any that fail, providing a self-healing mechanism to address machine failure or maintenance.

### Container Requirements

Applications must be packaged into a supported container format to be deployed on Kubernetes. When creating a Deployment, you specify the container image and the number of replicas. The tutorial uses `gcr.io/google-samples/kubernetes-bootcamp:v1`.

### kubectl Syntax

Common format: `kubectl action resource`
- Use `--help` after any subcommand for additional info (e.g., `kubectl get nodes --help`)

### Network Privacy

Pods run on a private, isolated network — visible within the cluster but not outside. `kubectl proxy` creates a proxy that forwards communications into the cluster-wide private network. The API server creates an endpoint for each pod based on its pod name.

---

## Commands

```bash
# Check kubectl version and cluster connectivity
kubectl version

# View nodes in the cluster
kubectl get nodes

# Create a Deployment
kubectl create deployment kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1

# List deployments
kubectl get deployments

# Start proxy to access the private network (run in separate terminal)
kubectl proxy

# Check API version via proxy
curl http://localhost:8001/version

# Get Pod name into a variable
export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\\n"}}{{end}}')
echo Name of the Pod: $POD_NAME

# Access Pod through proxied API
curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME:8080/proxy/
```

---

## What create deployment does

1. Searched for a suitable node where an instance of the application could run.
2. Scheduled the application to run on that Node.
3. Configured the cluster to reschedule the instance on a new Node when needed.

---

## Notes

- Without a Service, the Deployment is not accessible from outside the cluster without using the proxy.
- Services are covered in a later tutorial (Expose Your App Publicly).
