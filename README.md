# k8s-assistant

An interactive Kubernetes learning assistant that explores your live cluster environment and guides you through official [kubernetes.io tutorials](https://kubernetes.io/docs/tutorials) step by step.

## What it does

- Discovers your current `kubectl` context and running workloads
- Maps your question to the most relevant tutorial module
- Guides you through exercises with full `kubectl` access (get, apply, create, delete, scale, rollout, etc.)
- Recaps concepts at the end of each session

## Install

Symlink the `skill/` directory into your agent skills directory:

```bash
# Global
ln -s ~/repos/k8-assistant/skill ~/.agents/skills/k8s-assistant

# Project-scoped
ln -s ~/repos/k8-assistant/skill ~/repos/<your-project>/.agents/skills/k8s-assistant
```

## Repository layout

| Path                              | Purpose                                              |
|-----------------------------------|------------------------------------------------------|
| `skill/SKILL.md`                  | Skill definition (frontmatter + instructions)        |
| `skill/references/tutorial-map.md`| 26-module tutorial map with tags and links           |
| `docs/wiki/`                      | Maintainer knowledge base — not loaded at runtime    |
| `docs/adr/`                       | Architectural decision records                       |
| `tools/extract.py`                | Extraction script for ingesting kubernetes.io pages  |
