<!--
  Source : https://github.com/bayer-int/csgdaa-skills/pull/16#issuecomment-3762777148
  Author : stephen.mcelhose.ext
  Date   : 2026-01-14 (comment); ingested 2026-08-07
  Note   : Manually authored tag taxonomy covering all 26 k8s tutorial topics.
           Organised into 30 thematic categories. Used as authoritative tag reference
           for kubernetes-topic-taxonomy.md and wiki page frontmatter.
  Do NOT edit. Re-fetch from source if updates are needed.
-->

# Tags

## Core kubectl
kubectl
command
syntax
alias
shortcut
reference
documentation
best-practices

## Configuration & Context
configuration
context
kubeconfig
use-context
set-context
current-context
namespace

## Basic Commands (Imperative)
create
apply
get
describe
delete
edit
patch
run
expose
label
annotate
scale
rollout
set

## Output & Filtering
output
format
json
yaml
jsonpath
custom-columns
wide
watch
selector
field-selector
sort-by

## Debugging & Troubleshooting
logs
exec
port-forward
proxy
debug
troubleshooting
events
top
attach

## Workloads - Deployments
deployment
replicaset
pod
container
image
replica
strategy
pause
resume

## Workloads - StatefulSets
statefulset
headless-service
volumeclaimtemplate
ordinal
stable-identity
stable-network-id
stable-storage

## Workloads - Jobs & CronJobs
job
cronjob
completions
parallelism
backoff-limit

## Workloads - Init & Sidecar Containers
init-container
sidecar
feature-gate
restartpolicy
lifecycle

## Services & Networking
service
clusterip
nodeport
loadbalancer
externalname
endpoint
endpointslice
dns
port
targetport
nodeport-range

## ConfigMaps & Secrets
configmap
secret
volume
env
envfrom
key
value
immutable

## Storage
persistentvolume
persistentvolumeclaim
storageclass
accessmode
reclaimpolicy
provisioner
dynamic-provisioning

## Pod Lifecycle & Termination
prestop
terminationgraceperiodseconds
endpoint-conditions
graceful-shutdown
connection-draining
serving
ready
terminating

## Node Management
taint
cordon
drain
uncordon

## Scaling & Load Balancing
autoscale
load-balancing
rolling-update
partition
canary

## Security - RBAC
security
rbac
authentication
authorization
clusterrole
clusterrolebinding

## Security - Pod Security
pod-security
admission-controller
baseline
restricted
privileged
enforce
warn
audit

## Security - Advanced
security-context
apparmor
seccomp
profile
syscall
runtime-default
tls
openssl

## Cluster Management
cluster
cluster-info
api-resources
api-versions
version
minikube
kubeadm
kind

## Container Runtime & Low Level
kubelet
standalone
container-runtime
cri-o
crio
crun
runc
crictl
systemd
static-pod
cni
network-plugin
journalctl

## Resource Allocation
dra
dynamic-resource-allocation
deviceclass
resourceslice
resourceclaim
resourceclaimtemplate
device-plugin
cdi
cel

## Swap Configuration
swap
swapon
swapoff
sysctl
fallocate
mkswap
cryptsetup
swapbehavior
limitedswap
failswapon

## Networking Details
networking
source-ip
nat
snat
dnat
vip
kube-proxy
iptables
externaltrafficpolicy
healthchecknodeport

## Deployment Patterns
imperative
declarative
feature-gate
immutable
dry-run
wait
kustomize

## Automation & Tooling
script
automation
plugin
completion
bash
zsh
fish

## Application Examples - Stateless
guestbook
frontend
backend
tier
role

## Application Examples - Stateful
redis
redis-cli
cassandra
nodetool
seed
ring
zookeeper
zkCli
quorum
ensemble
consensus
zab
leader-election
myid
ruok
wordpress
mysql
follower
leader
ordinal
podantiaffinity

## Testing & Utilities
curl
wget
nslookup
ssh
localhost
production
resource-type
annotation
