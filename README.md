# k8s-assistant

A [csgdaa-code](https://github.com/bayer-int/csgdaa-code) skill that acts as an interactive Kubernetes learning assistant. It explores your live cluster environment and guides you through official [kubernetes.io tutorials](https://kubernetes.io/docs/tutorials) step by step.

## What it does

- Discovers your current `kubectl` context and running workloads
- Maps your question to the most relevant tutorial module
- Guides you through exercises with full `kubectl` access (get, apply, create, delete, scale, rollout, etc.)
- Recaps concepts at the end of each session

## Install as a skill

### Option A — symlink (local dev, edits reflect immediately)

```bash
ln -s ~/repos/k8-assistant ~/.agents/skills/k8s-assistant
# or for a specific project:
ln -s ~/repos/k8-assistant ~/repos/<your-project>/.agents/skills/k8s-assistant
```

### Option B — csgdaa-code CLI (once published to a catalog)

```bash
csgdaa-code add k8s-assistant
```

## Dev setup (working on the skill itself)

Install the dev skills locally — they are gitignored and won't be committed:

```bash
mkdir -p .agents/skills
csgdaa-code add skill-creator
csgdaa-code add llm-wiki
```

Or copy them manually from another project's `.agents/skills/`.

## Files

| Path                              | Purpose                                         |
|-----------------------------------|-------------------------------------------------|
| `SKILL.md`                        | Skill definition (frontmatter + instructions)   |
| `references/quick-reference.md`   | kubectl command cheatsheet                      |
| `references/tutorial-map.md`      | 26-module tutorial map with context scores      |
| `docs/pr-notes.md`                | Notes from original csgdaa-skills PR #16        |
