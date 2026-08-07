---
type: concept
title: Learning Aid Rubric
description: A 6-criterion, 100-point pedagogical scoring framework for evaluating the k8s-assistant skill's effectiveness as a learning tool for developers and novice DevOps engineers.
resource: docs/wiki/skill-design-principles.md
tags: [pedagogy, evaluation, learning, rubric, scoring]
timestamp: 2026-08-07T15:39:38Z
---

# Learning Aid Rubric

A rubric for evaluating the k8s-assistant as a pedagogical tool. It targets developers and novice DevOps engineers learning Kubernetes deployment troubleshooting.

This rubric serves two purposes:
1. **Retrospective** — score the current skill against each criterion to find gaps
2. **Composition** — potentially embed as a self-evaluation prompt within the skill, or use as a standalone overlay when a maintainer wants to assess a new skill version

See also [[skill-design-principles]] for the design decisions that informed this rubric, and [[tutorial-coverage-scoring]] for the complementary per-tutorial scoring system.

## Criteria

| Criterion                     | Weight | What "4 (Excellent)" looks like                                                       |
|-------------------------------|--------|---------------------------------------------------------------------------------------|
| Engagement & Motivation       | 20%    | Scenarios resonate with real challenges; encourages active participation               |
| Relevance to Audience         | 20%    | Directly addresses developer/novice DevOps pain points; builds practical skills        |
| Ease of Understanding         | 15%    | Simple language; builds progressively; assumes appropriate prior knowledge             |
| Practical Application         | 20%    | Hands-on, actionable examples the learner can immediately apply                        |
| Support for Learning Outcomes | 15%    | Clear measurable objectives; demonstrable skill improvement in troubleshooting         |
| Feedback & Assessment         | 10%    | Self-checks, progression indicators, ways for learners to gauge their own progress     |

Scores are 1–4 per criterion, multiplied by weight, summed to 100.

## Score thresholds

| Range   | Rating                                  |
|---------|-----------------------------------------|
| 90–100  | Excellent learning aid                  |
| 70–89   | Good — room for improvement             |
| 50–69   | Fair — significant revisions needed     |
| < 50    | Poor — major overhaul required          |

## Notes on application

- The rubric is **domain-agnostic** — it can be reused to evaluate any tutorial-guided skill, not just k8s-assistant.
- The heaviest weights (Engagement, Relevance, Practical Application — 60% combined) reflect that a technically accurate but dry skill fails learners even if the content is correct.
- **Feedback & Assessment** (10%) is the most underdeveloped criterion in the current skill. The session recap at the end (`## Post-Condition` in `SKILL.md`) is the only mechanism. See [[skill-design-principles]] for ideas.

## Sources

- `docs/wiki/skill-design-principles.md` — design decisions that informed this rubric
