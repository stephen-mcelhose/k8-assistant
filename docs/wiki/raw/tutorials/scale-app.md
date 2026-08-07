# Running Multiple Instances of Your App

Source: https://kubernetes.io/docs/tutorials/kubernetes-basics/scale/scale-intro/
Fetched: 2026-08-07

---

## Objectives

- Scale an existing app manually using `kubectl`.

---

## Before You Begin

- POSIX shell (bash, zsh, sh). Windows → WSL or Git Bash.
- Assumes Tutorial #2 (Deploy an App) Deployment is running.
- Requires a Service of type LoadBalancer. If the Service from Tutorial #4 was deleted, recreate:
  ```bash
  kubectl expose deployment/kubernetes-bootcamp --type="LoadBalancer" --port 8080
  ```

---

## Key Concepts

### Scaling

Scaling changes the number of replicas in a Deployment. Kubernetes creates new Pods and schedules them to Nodes with available resources.

- Scale out: increases replica count, new Pods scheduled
- Scale down: terminates excess Pods
- Scale to zero: terminates all Pods (Deployment object remains)
- Autoscaling (HPA) is also supported but outside this tutorial's scope

### ReplicaSets

A ReplicaSet is the mechanism under a Deployment that ensures the desired number of replicas are running at any time. Deployment manages the ReplicaSet; users interact with the Deployment, not the ReplicaSet directly.

ReplicaSet name format: `[DEPLOYMENT-NAME]-[RANDOM-STRING]` (random string seeded from `pod-template-hash`)

### Load Balancing

Services have an integrated load balancer that distributes traffic to all Pods of an exposed Deployment. Services monitor Pods via endpoints and route traffic only to available Pods. Multiple replicas + a Service = automatic load balancing.

---

## Commands

```bash
# Check current deployments (shows READY, UP-TO-DATE, AVAILABLE counts)
kubectl get deployments

# View the ReplicaSet created by the Deployment
kubectl get rs

# Scale up to 4 replicas
kubectl scale deployments/kubernetes-bootcamp --replicas=4

# Verify new pods (shows IPs and node assignments)
kubectl get pods -o wide

# Describe deployment to confirm replica count and events
kubectl describe deployments/kubernetes-bootcamp

# Describe service to find exposed IP and port
kubectl describe services/kubernetes-bootcamp

# Capture NodePort into an env variable
export NODE_PORT="$(kubectl get services/kubernetes-bootcamp \
  -o go-template='{{(index .spec.ports 0).nodePort}}')"
echo NODE_PORT=$NODE_PORT

# Curl the app repeatedly — observe different Pod names in response
curl http://$(minikube ip):$NODE_PORT

# Scale down to 2 replicas
kubectl scale deployments/kubernetes-bootcamp --replicas=2

# Verify pods terminated
kubectl get pods -o wide
```

---

## Notes

- `kubectl get deployments` columns: NAME, READY (current/desired), UP-TO-DATE, AVAILABLE, AGE
- `kubectl get rs` columns: NAME, DESIRED, CURRENT, READY, AGE
- Docker Desktop driver on macOS requires `minikube tunnel` or `minikube service <name> --url` to access NodePort services
- Rolling updates (Tutorial #6) become downtime-free when multiple replicas are running
