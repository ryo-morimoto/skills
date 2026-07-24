---
name: splitting-changes
description: Decomposes tangled requirements, plans, large tasks, diffs, pull requests, commits, migrations, and releases into the smallest independently deliverable change units, then validates single concern, dependency order, testability, deployability, and reversibility. Use when a user asks to split requirements or implementation work, reduce an oversized task or PR, create staged or stacked delivery, plan an incremental migration, untangle mixed changes, or decide the minimum safe/value-bearing slice—even if they do not explicitly say “split.”
---

# Splitting Changes

Turn a complex change into a sequence of cohesive, independently verifiable units. Optimize for one concern and safe delivery; treat line count only as a warning signal.

## Core principles

- Define “minimum” in three ways: minimum value, minimum safe step, and economically sensible batch.
- Prefer a unit whose intent can be stated in one sentence without joining distinct concerns.
- Preserve a dependency DAG and a valid landing order.
- Keep structure-only changes separate from behavior changes.
- Keep every landed state buildable, testable, deployable, and reversible when the system permits it.
- Include cleanup such as flag removal or contract steps as explicit units.
- Use size thresholds as prompts to inspect cohesion, never as automatic rejection rules.
- Treat automated untangling as a proposal. Require human confirmation before applying or publishing the resulting change series.

## Workflow

### Frame the outcome

State the overall goal, affected users or systems, non-negotiable constraints, and the riskiest uncertainty. Distinguish:

- requirement slicing: decide what value or learning can ship first;
- implementation sequencing: decide how to land safely;
- calibration: decide whether the team’s batch size is economically effective.

Read [references/value-slicing.md](references/value-slicing.md) for requirements or release scope. Read [references/safe-steps.md](references/safe-steps.md) for code, migrations, refactors, or large diffs.

### Generate candidate units

For each unit, capture:

- one-sentence intent;
- standalone value or learning;
- estimated cost;
- predecessor units;
- change kind and affected targets;
- build, test, and deploy evidence;
- rollback or disable path;
- estimated changed lines as a warning-only signal.

Use the JSON contract in [references/plan-format.md](references/plan-format.md) when a machine-checkable plan is useful.

### Select the first value-bearing slice

Choose a thin end-to-end slice that crosses the core uncertainty. Reduce one variation axis at a time—rule, data, path, interface, or user type—without replacing the slice with horizontal component work. Make dependencies explicit before optimizing order.

### Derive safe landing steps

Build a dependency graph. When prerequisites are unclear, try the target change, record what breaks as prerequisite nodes, revert the probe, and repeat until leaf steps are visible. Land leaves before roots.

Use expand–migrate–contract, branch by abstraction, feature flags, or a strangler boundary when compatibility requires multiple states. Add the removal step to the plan.

### Apply the gates in order

1. **Single concern [A-informed]**: confirm one logical intent and one dependency cluster. Reject explicit mixtures of structural and behavioral change.
2. **Independent verification [B-informed/normative]**: confirm each unit can be built, tested, and deployed alone, or document why a transition strategy makes that possible.
3. **Dependency health [normative]**: confirm an acyclic graph and topological landing order.
4. **Reversibility [normative]**: provide revert, flag-off, rollback, or forward-fix guidance.
5. **Size [C-informed warning]**: inspect oversized units for hidden concerns; do not reject solely by line count.

For the evidence boundaries behind these labels, read [references/evidence.md](references/evidence.md).

### Validate and revise

Run:

```bash
python3 scripts/validate_split_plan.py split-plan.json
```

Fix errors, review warnings, and rerun until the plan passes. Use `--strict` only when the team has chosen to make warnings blocking. Never silently apply an LLM-generated split.

### Present the result

Return:

1. the overall goal and chosen first slice;
2. an ordered unit table with intent, value, dependencies, verification, rollback, and size estimate;
3. explicit assumptions and unresolved decisions;
4. validator errors or warnings and how they were handled;
5. calibration suggestions only when team delivery data is available.

Avoid splitting work that is already one small, cohesive, independently verifiable concern. Avoid presenting component-layer tasks as value slices unless they are prerequisites in a safe landing sequence.

## Calibration

Read [references/delivery-metrics.md](references/delivery-metrics.md) only when evaluating team-wide batch policy, PR-size warnings, review latency, or delivery performance. Do not import a universal line threshold or optimize deployment frequency in isolation.
