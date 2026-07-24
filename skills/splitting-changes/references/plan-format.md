# Split-plan JSON format

Use this format with `scripts/validate_split_plan.py`.

## Contents

- [Example](#example)
- [Required fields](#required-fields)
- [Exit behavior](#exit-behavior)

## Example

```json
{
  "goal": "Release email sign-in without breaking password sign-in",
  "warning_line_threshold": 400,
  "units": [
    {
      "id": "u1",
      "intent": "Add a backward-compatible nullable email identity",
      "value": "Enables migration without changing current sign-in behavior",
      "estimated_cost": 2,
      "depends_on": [],
      "change": {
        "kind": "structure",
        "targets": ["users.email", "identity lookup"],
        "single_cluster": true
      },
      "independence": {
        "build": {
          "possible": true,
          "evidence": "make build"
        },
        "test": {
          "possible": true,
          "evidence": "pytest tests/test_identity.py"
        },
        "deploy": {
          "possible": true,
          "evidence": "nullable field is backward compatible"
        }
      },
      "delivery_strategy": "expand",
      "rollback": "Revert the migration before any email identities are written",
      "estimated_lines": 120
    },
    {
      "id": "u2",
      "intent": "Remove the legacy identity lookup after migration",
      "value": "Eliminates the temporary compatibility path",
      "estimated_cost": 1,
      "depends_on": ["u1"],
      "change": {
        "kind": "contract",
        "targets": ["legacy identity lookup"],
        "single_cluster": true
      },
      "independence": {
        "build": {
          "possible": true,
          "evidence": "make build"
        },
        "test": {
          "possible": true,
          "evidence": "pytest tests/test_identity.py"
        },
        "deploy": {
          "possible": true,
          "evidence": "migration completion check"
        }
      },
      "delivery_strategy": "contract",
      "contract_for": "u1",
      "rollback": "Restore the compatibility lookup",
      "estimated_lines": 80
    }
  ],
  "landing_order": ["u1", "u2"]
}
```

## Required fields

Top level:

- `goal`: non-empty string.
- `units`: non-empty array.
- `landing_order`: every unit ID exactly once in dependency-safe order.
- `warning_line_threshold`: optional positive number; defaults to 400.

Each unit:

- `id`: unique non-empty string.
- `intent`: one-sentence logical intent.
- `value`: standalone value, safety, or learning.
- `estimated_cost`: non-negative number or non-empty qualitative string.
- `depends_on`: array of unit IDs.
- `change.kind`: one of `structure`, `behavior`, `data`, `docs`, `test`, `operations`, `cleanup`, `expand`, or `contract`. Do not use `mixed`.
- `change.targets`: non-empty array of affected concepts or paths.
- `change.single_cluster`: boolean assessment.
- `independence.build`, `.test`, and `.deploy`: each contains `possible` and `evidence`.
- `delivery_strategy`: `direct`, `flag`, `expand`, `contract`, `strangler`, `branch-by-abstraction`, or `not-applicable`.
- `rollback`: non-empty string.
- `estimated_lines`: non-negative number.

For `contract`, set `contract_for` to the expanded or flagged unit it cleans up. Expand or flag strategies without a corresponding contract/removal unit produce warnings.

## Exit behavior

- Exit `0`: no errors. Warnings may remain.
- Exit `1`: validation errors exist, or warnings exist with `--strict`.
- Use `--json-output` for structured diagnostics.
