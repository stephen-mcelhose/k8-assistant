---
type: concept
title: Skill Design Principles
description: The design intent behind k8s-assistant — the novel environment framing, discover-then-guide workflow, and pedagogical choices that shape the skill's behaviour.
resource: skill/SKILL.md
tags: [skill-design, pedagogy, architecture, workflow, environment-discovery]
timestamp: 2026-08-07T15:39:38Z
---

# Skill Design Principles

The k8s-assistant is built around a specific philosophy: **meet the learner where they are, not where you expect them to be**. This page captures the design decisions that follow from that.

## The "novel environment" framing

The skill's description says "in a novel environment" deliberately. The agent doesn't assume the learner has minikube, a managed cloud cluster, or any particular setup. Instead, it discovers:

1. Is `kubectl` present? If not, redirect to Getting Started.
2. What context is active? (`kubectl config current-context`)
3. What's running in the current namespace? (`kubectl get pods,svc,deploy`)

Only after this discovery does it ask what the learner wants to do. This prevents the agent from giving tutorial instructions that don't match the learner's actual environment (e.g., recommending a LoadBalancer tutorial to someone on a bare-metal cluster).

See [[security-considerations]] for the credential-exposure risk associated with `kubectl config view` in this step.

## Discover → Align → Guide

The four-step workflow in `SKILL.md`:

1. **Environment Discovery** — understand the cluster, context, and current workloads
2. **Objective Setting** — map the user's question to the highest-scoring tutorial (see [[tutorial-coverage-scoring]])
3. **Guided Learning** — hints for simple tasks; step-by-step with "why" for complex ones
4. **Reference Usage** — pull from `quick-reference.md` and `kubectl get -o yaml` for deep inspection

The key pedagogical choice in step 3: **hints over answers for simple tasks**. The skill encourages discovery rather than just executing commands on the learner's behalf. For complex tasks it switches to full walkthroughs, because at that point the cognitive load of figuring it out alone would overwhelm rather than teach.

## Tutorial alignment over free-form Q&A

The skill deliberately anchors to official kubernetes.io tutorials rather than answering Kubernetes questions generally. This:
- Ensures the learner gets authoritative, maintained content
- Makes the session reproducible (another agent running the same skill would give structurally similar guidance)
- Constrains the scope so the skill doesn't drift into a generic K8s assistant

The [[kubernetes-topic-taxonomy]] and [[tutorial-coverage-scoring]] systems exist to make this alignment precise.

## Session recap as the only assessment mechanism

The `## Post-Condition` step — a concise recap of all concepts and resources explored — is the skill's only feedback/assessment mechanism. The [[learning-aid-rubric]] gives this criterion (Feedback & Assessment) a weight of 10% and notes it's the weakest point. Potential improvements:
- Ask the learner a reflection question at the end ("What would you do differently if you saw this error again?")
- Surface a follow-up tutorial suggestion with its context score
- Optionally write a session summary to a local file for the learner's reference

## What the skill intentionally does not do

- **No cluster state management** — the skill guides learning, it doesn't own the cluster
- **No persistent memory between sessions** — each session starts fresh with environment discovery
- **No free-form Kubernetes Q&A** — questions that don't map to a tutorial are redirected to the tutorial map

## Sources

- `skill/SKILL.md` — the skill definition itself
