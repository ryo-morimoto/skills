# Safe implementation steps

Use this guide for large diffs, refactors, migrations, legacy changes, stacked PRs, or work whose prerequisites are unclear.

## Discover the dependency graph

1. State the target behavior in one sentence.
2. Attempt the most direct change as a disposable probe.
3. Record each compilation failure, test failure, compatibility break, or missing abstraction as a prerequisite node.
4. Revert the probe.
5. Repeat on each prerequisite until leaf changes can land safely.
6. Topologically order the graph from leaves to the target behavior.

The probe is for learning. Do not leave a broken intermediate state in the delivery series.

## Enforce single concern

For every unit:

- Align the intent, diff, test, and commit message.
- Keep one semantic purpose.
- Confirm affected hunks form one dependency cluster.
- Separate rename, formatting, generated output, or mechanical movement from behavior changes when the separation improves review.
- Separate structural preparation from behavioral change.
- Keep tests with the behavior they verify when needed for independent verification; do not mechanically split tests into another unit.

Line count is secondary. A large mechanical unit can be cohesive; a five-line unit can mix concerns.

## Compatibility patterns

### Expand–migrate–contract

1. Expand the interface or schema compatibly.
2. Migrate callers or data incrementally.
3. Verify old and new paths.
4. Contract by removing the old path.

Represent contract as an explicit unit. Do not leave permanent compatibility scaffolding by omission.

### Branch by abstraction

Introduce an abstraction around the old implementation, add the new implementation behind it, switch callers, then remove the old implementation and temporary abstraction if no longer useful.

### Feature flag

Land dormant behavior, test it safely, enable progressively, then remove the flag and dead path. Record flag ownership, default state, rollback action, and removal condition.

### Strangler boundary

Route one behavior or traffic segment to the new path, observe it, expand coverage, and retire the replaced path.

## G2 implementation gate

- **Single concern**: one intent; no explicit structure-and-behavior mixture.
- **Independent verification**: a concrete build/test command or equivalent evidence.
- **Deployability**: direct landing or a named transition strategy.
- **DAG**: all predecessors exist; no cycle; landing order is topological.
- **Reversibility**: revert, disable, rollback, or forward-fix path.
- **Cleanup**: every expand or flag step has a contract/removal unit.
- **Size**: oversized units trigger inspection, not automatic rejection.

Automated hunk clustering can suggest units, but semantic intent and hidden runtime dependencies require review. Present uncertain groupings explicitly for confirmation.
