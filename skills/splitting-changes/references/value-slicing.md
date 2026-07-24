# Value slicing

Use this guide for tangled requirements, product scope, release planning, and “what can ship first?” questions.

## Default method

1. Name the user or operator and the desired outcome.
2. Identify the core uncertainty that could invalidate the approach.
3. Map the end-to-end path from input to observable outcome.
4. List variation axes: business rule, data shape, path, interface, user type, quality level, and exception.
5. Hold most axes to one simple case and retain one complete path.
6. Describe the slice in one sentence: “For [actor], enable [outcome] under [narrow condition] so that [value or learning].”
7. Assign value, estimated cost, and precedence dependencies.
8. Choose the smallest dependency-closed set that produces value or learning.

Do not call database-only, API-only, or UI-only layers “value slices” unless they independently produce an observable outcome. They may still be necessary safe steps.

## Candidate-splitting lenses

- **Spike**: isolate a time-boxed learning result when uncertainty dominates.
- **Path**: support one workflow path before alternatives.
- **Interface**: support one entry point before others.
- **Data**: support one data category or shape.
- **Rules**: support one business rule before variants.
- **User type**: support one actor or permission group.
- **Quality level**: deliver a deliberately narrow service level before optimization.

Prefer one default lens. Combine lenses only if one does not expose a viable end-to-end slice.

## G1 planning gate

Ask:

- Can the unit’s standalone value or learning be stated in one sentence?
- Does the first slice cross the core uncertainty rather than avoid it?
- Is the unit reasonably independent and negotiable?
- Is its value explicit and its size estimable?
- Is it testable with an observable acceptance condition?
- Are value, cost, and precedence dependencies present?

INVEST is a practical heuristic, not a controlled-experiment result. Use it to prompt discussion, not to manufacture a numeric truth.

## Dependency-closed selection

Treat candidate units as a directed graph. Selecting a unit also selects all of its predecessors. Compare feasible sets by:

- value or learning delivered;
- estimated effort and delay;
- risk retired;
- irreversible commitments introduced.

Use exact optimization only when the decision warrants the modeling cost. For normal planning, validate the DAG, enumerate a few dependency-closed options, and explain the tradeoff.

## Output shape

Provide:

| Order | Unit | Standalone value/learning | Cost | Depends on | Acceptance |
| --- | --- | --- | --- | --- | --- |

Then state why the first dependency-closed set is sufficient and what is intentionally deferred.
