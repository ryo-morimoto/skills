# Deterministic calculator

Python 3.9+ standard library only. Run from the project root. All data enters stdin;
JSON or Markdown leaves stdout. Errors are JSON on stderr, exit 2, no traceback.
No output files, target-code imports, expressions, subprocesses, or networking are
used by the calculator. File redirection below reads only the bundled example.

```sh
python3 -B skills/refactor-options/scripts/compare.py --help
python3 -B skills/refactor-options/scripts/compare.py describe --type plan_result
python3 -B skills/refactor-options/scripts/compare.py describe --type planning
python3 -B skills/refactor-options/scripts/compare.py validate --type decision_packet < skills/refactor-options/assets/example-portfolio.json
python3 -B skills/refactor-options/scripts/compare.py render < skills/refactor-options/assets/example-portfolio.json
python3 -B skills/refactor-options/scripts/compare.py validate --type decision_packet < skills/refactor-options/assets/example-decision.json
python3 -B skills/refactor-options/scripts/compare.py compare < skills/refactor-options/assets/example-decision.json
python3 -B skills/refactor-options/scripts/compare.py compare --horizons 6 12 13 14 24 < skills/refactor-options/assets/example-decision.json
python3 -B skills/refactor-options/scripts/compare.py render < skills/refactor-options/assets/example-decision.json
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s skills/refactor-options/tests -p 'test_*.py' -v
```

`validate --type TYPE` accepts any named bundled `$defs`, including
`shared_context`, `strategy_task`, `plan_result`, `critique_result`,
`decision_packet`, `run_record`, `range`, `evidence`, `design_review`, `planning`.
`describe` returns that definition and its transitive dependencies. Standalone
components cannot verify external IDs/revisions/evidence: the full
`decision_packet` is the source of truth for cross-component checks. In particular,
standalone `planning` derives its plan IDs from assignments and cannot know which
real plans were omitted or whether its evidence IDs exist in the context registry.

## Contract details

- JSON Schema is a **limited local subset**, not a general-purpose implementation:
  `$schema`, `$ref` (local `$defs` only), `$defs`, `type`, `required`, `properties`,
  boolean `additionalProperties`, `items`, `minItems`, `maxItems`, `minLength`,
  `minimum`, `maximum`, `pattern`, `enum`, `const`, plus `description`/`title`.
  Unsupported keywords fail closed. No remote schema retrieval. All core objects
  reject extra fields. Non-finite numbers, duplicate JSON keys, boolean numbers,
  mixed-null or reversed ranges fail.
- Unit spellings are exact: costs/recovery `person_hour`, savings
  `person_hour/month`, completion `month`. Generic ranges can name other units;
  the calculator does not convert them or compare incompatible quantities.
  Known ranges need evidence/assumption IDs. All-null ranges need a reason.
- Cost completeness means every **declared** component is known and at least one
  component exists. Unestimated work must be an explicit unknown component;
  omission/double-counting cannot be discovered mechanically. Incomplete costs
  retain `known_subtotal`, `total: null`, and never produce capacity. Empty costs
  have a zero additive subtotal, explicitly incomplete, **not a zero total**.
- Components add independently within low/reference/high scenarios; these are
  not confidence intervals. Net capacity reference is `b * max(0,H-m) - C`.
  Low combines low savings/high completion/high cost; high reverses those inputs.
  Completion may exceed the horizon: benefit then remains zero, cost still applies.
  Capacity requires all known inputs and the context's common horizon. Constant
  savings are a declared simplifying assumption, not a universal impact model.
- Sensitivity defaults to H−1, H, H+1, clamped at zero. `--horizons` replaces the
  sensitivity list, not the primary context horizon. Reference-line break-even
  is reported only at/after both completion times. No probabilities, currency,
  total score, automatic recommendation/selection, risk arithmetic, or Pareto
  claims/frontier are computed. All change plans and P0 remain present. Portfolio
  change-plan pairs are `not_comparable`, with null crossover and an explanation
  of different/nonexclusive objectives, even when reference inputs are known.
  P0-versus-plan comparison remains standalone incremental baseline capacity.
- Missing/unknown hard gates or incomplete status mean `conditional`; failing
  gates or infeasible status mean `excluded`. Blocking critique excludes affected
  plans; major critique makes them conditional (null plan ID affects all).
  An excluded plan cannot be selected/recommended. Conditional recommendations
  need conditions. Unknown cost alone is not a failed hard gate: capacity remains
  unknown. The comparison does not assert that an admissible design is verified.
- New final packets use `schema_version: "1.1"`, context version `1.1`, at least
  **three change proposals excluding P0**, `planning`, and `critique.design_review`.
  Four or more proposals are supported without an upper limit. Two plus P0 cannot
  complete a new packet; preserve incomplete research in prose outside the final
  packet instead. Current context revisions and a critique of every exact plan
  revision including P0 are required. Baseline costs/savings/completion are known
  zero **deltas**; ongoing maintenance/risk still belong in its narrative and risks.
- Historical schema `1.0` remains accepted with **two to three** change plans,
  optional design review, no `planning` or selection `plan_ids` fields. Legacy
  examples and saved assessments are not migrated. Rendering adds an explicit
  legacy count/mode warning without altering source data or historical math.
  Packet/context versions accept only `1.0` and `1.1`. Version-specific constraints
  live in semantic validation, not JSON Schema conditionals: schema validation alone
  is insufficient. `validate` reports the supplied packet/context schema version;
  unversioned standalone components retain the historical `1.0` acknowledgement.
- At least one recorded completed planner batch must cover all change
  strategies in distinct context IDs; an independent completed critic is required.
  Non-viable attempted strategies count structurally, not as viable choices.
  Rendering separates declared viable/infeasible/incomplete counts from
  admissible/conditional/excluded counts; duplicates are not three valid,
  independent options. Failed records may remain but do not satisfy
  completion. All records use the current revision; historical records belong in
  separately retained host logs. Call IDs are unique. Assertions cannot establish
  actual chronology, parallelism, distinct strategy quality, evidence truth,
  sandboxing, or that a human answer really came from the user.
- In legacy or `alternatives` mode, pending decisions have null plan/answer;
  selected decisions need a valid,
  non-excluded plan and explicit answer; deferred/rejected need an answer and null
  plan. Every decision uses the current context revision. No selection is inferred
  from a recommendation. Dependencies can reference later-listed steps; missing
  dependencies and cycles fail. ID uniqueness is per registry/plan, not global
  across unrelated namespaces.
- `assessment` is optional and calculator-owned (`formula_version: "1.0"`).
  `compare`, `validate --type decision_packet`, and `render` verify existing
  assessments against raw inputs, rejecting stale/tampered values. Remove an old
  assessment explicitly before recomputing changed source data. `render` also
  accepts raw packets and recomputes. Its static structure comes only from
  `assets/decision-template.md`; all raw per-plan fields, evidence, contracts,
  steps, recovery, critique and decision state are retained and Markdown-escaped.

## Planning modes and portfolio selection (skill 0.3)

`planning` has exactly these fields; every object rejects extras:

```text
{
  mode: "alternatives" | "portfolio",
  areas: [{id, name, scope: [text], objective, success_scenarios: [text]}],
  assignments: [{plan_id, area_ids: [text], depends_on: [plan_id]}],
  relations: [{plan_ids: [left, right],
    relationship: "alternative" | "complementary" | "independent" | "unknown",
    compatibility: "compatible" | "conflicting" | "unknown",
    benefit_overlap: "disjoint" | "shared" | "unknown", reason, evidence_ids: [text]}]
}
```

- At least one area; each has nonempty scope and success scenarios. All planning
  text, including identifiers and reasons, must be nonblank, not whitespace-only.
  Assign **every change plan exactly once**; never assign P0. Area IDs are unique
  and known, nonempty per assignment, and every area has at least one candidate.
- `alternatives` requires exactly one area, empty prerequisites and relationship
  `alternative` for every pair. Existing single `plan_id` selection semantics
  remain; optional `plan_ids` must be absent or `[]`.
- `portfolio` requires at least two areas. A plan may span multiple areas. Plan
  prerequisites use known change-plan IDs, never P0, self or duplicates, and form
  a DAG; forward references are allowed.
- Exactly one relation covers each unordered change-plan pair: three plans need
  three pairs, four need six. P0, self-pairs, unknown IDs, missing pairs and reversed
  duplicates fail. Evidence IDs are checked against the full packet registry.
  Different areas **do not imply** independence, compatibility or disjoint benefits.
  Relations are explicit review assertions, independent of design diversity.
- In portfolio mode, both recommendation and decision **require** `plan_ids`
  (possibly `[]`) and `plan_id: null`. IDs must be unique known change plans, never
  P0 or excluded plans. Recommendations and selected sets include all transitive
  prerequisites and cannot contain conflicting or `alternative` pairs.
- A recommendation containing any conditional plan or unknown-compatibility pair
  needs nonempty, nonblank `conditions`. Unknown compatibility does not automatically
  prohibit human selection; rendering explicitly warns that composition is not
  established safe. No recommendation or selection is inferred from numbers.
- Pending/deferred/rejected portfolio decisions require `plan_ids: []`. Pending
  has `answer: null`; deferred/rejected require an explicit answer. Selected requires
  at least one ID, an explicit answer and the current context revision. Selection
  **does not grant implementation permission**.
- Rendering places planning before design and numbers, preserving escaped raw
  areas, assignments, prerequisites, relations and multi-ID decision fields. It
  distinguishes compatible assertions, unknown compatibility and conflicts.
  Design “Diversity” in a portfolio is **not proof of competing alternatives**.
- The calculator never sums costs, savings or capacities across a selected set.
  There is no combined portfolio estimate, implicit benefit-overlap deduction,
  scheduling model or universal ranking. Per-plan cost components still add as
  before; that is not permission to sum different plans.

`assets/example-portfolio.json` is a fully synthetic three-area, three-candidate
packet with all relations and design reviews, one prerequisite and unknown effort,
savings and duration. It is not real investigation, agent execution or composition
verification. `assets/example-decision.json` and `assets/example-design-review.json`
remain historical `1.0` fixtures.

## Structured design review (introduced in skill 0.2.0)

`critique_result.design_review` remains schema-optional for standalone critiques and
legacy `1.0` compatibility, but packet `1.1` requires it semantically. The design
review's own `version` and calculator `formula_version` remain `1.0`. Existing
capacity math, assessment shape and legacy computed assessments are unchanged.

- Shape: `{version:"1.0", pairwise:[...], plans:[...]}`. See
  `describe --type design_review` and `assets/example-design-review.json` (synthetic).
- Every unordered pair of change plans is required; P0 is excluded from pairwise
  diversity. Each pair has two unique IDs, a verdict, axes and a reason. Duplicate,
  reversed, missing or unknown-ID pairs fail validation. `distinct`/`overlapping`
  require at least one described axis; the program cannot verify its semantic merit.
- P0 and every change plan need exactly one individual review with six unique
  checks: `goal_fit`, `responsibility`, `dependencies`, `contract`, `migration`,
  `verification_recovery`. Each check has status, reason and evidence IDs.
- All checks passing permits `plausible`; any failing check requires `invalid`.
  `conditional` needs a conditional/unknown check without fail; `unknown` needs an
  unknown check without fail. These are static planning judgments, not test outcomes.
- `invalid` excludes a plan; `conditional`/`unknown` make it conditional. Duplicate
  pairs warn about insufficient diversity without automatically excluding either
  individually valid design. There is no numeric diversity or architecture score.
- The complete decision packet checks evidence references and reviewed revisions.
  Standalone critiques check coverage against their own reviewed-plan list, but
  lack the external evidence registry and source revisions to authenticate them.
- Rendering places the explicit pairwise/individual evaluation before numerical
  comparison. A legacy packet without it says design evaluation was not supplied;
  it is not retroactively validated. Existing legacy assessments still verify.

The normative rubric and verdict meanings are in `references/design-evaluation.md`.

The bundled example and its trace references are **synthetic**, never execution
proof. At H=12 references A=68, B=56 person-hours; they tie at H=13; at H=14
A=92, B=104. Risk severity remains a separate ordinal description.
