---
name: clarify-requirements-and-design
description: Use when a software request is vague, clarification is looping, basic-design drivers are unclear, quality attributes are underspecified, or 1–3 teams or partner companies need responsibility and interface boundaries. Convert uncertainty into decision-ready requirements, provisional design, an evidence plan, and the smallest useful E2E slice by routing semantics to questions, domain rules to examples, value to observation, feasibility to experiments, quality to scenarios, conflicts to decisions, and future unknowns to telemetry. Do not use for routine, already well-specified implementation or organization-wide transformation unless requirement or design uncertainty is the actual problem.
---

# Clarify Requirements and Design

Turn each material unknown into the cheapest evidence that can change a decision. Co-evolve requirements and design until one safe next action is executable; do not wait for complete requirements.

## Non-negotiable controls

| Control | Required behavior | Failure prevented |
|---|---|---|
| Separate knowledge states | Label `fact`, `assumption`, `hypothesis`, `decision`, and `unknown` | Accidental certainty |
| Ask selectively | Ask only when an answer exists now and different answers change the next action; ask at most one blocking question per round | Clarification loops |
| Match method to unknown | Route meaning to examples/questions, value to observation, feasibility to experiments, quality to scenarios, conflict to a decision owner, future state to telemetry | Using interviews to discover facts nobody knows |
| Keep examples conditional | State alternatives and the local evidence selecting among them | Example-driven architecture |
| Keep requested solutions provisional | Treat “make it async”, “use events”, “add an admin screen”, and similar requests as candidate means unless already approved as a binding constraint | User wording promoted into unsupported architecture |
| Design only consequential detail | Expand a view only if it can alter a boundary, data model, interface, technology, rollout, or operating model | Document completeness mistaken for design completeness |
| Scale to dependencies | Default to 1–3 teams or a partner; add coordination only for actual shared decisions and interfaces | Large-program ceremony |
| Bind investigations to decisions | Give every observation, prototype, spike, or benchmark a hypothesis, discriminating observation, decision, and stop rule | Research without convergence |
| Price irreversibility | Require stronger evidence for safety, law, security, contractual commitment, irreversible data loss, and expensive migration | Fast but high-loss commitments |
| Forbid invented completeness | Do not invent components, persistence, source of truth, queues, adapters, retries, timeouts, or thresholds | Familiar defaults presented as requirements |

## Execute the workflow

### 1. Inspect before asking

Read available specifications, code, diagrams, tickets, contracts, logs, analytics, support records, and prototypes. Retrieve facts already present; do not make the user restate them.

### 2. Frame outcome and scope

Write one provisional sentence:

```text
<actor> changes <current behavior/state> to <observable behavior/state>, under <material constraints>.
```

Keep the requested feature or architecture as a candidate solution unless evidence establishes it as a constraint. Mark missing terms; do not block on them yet.

Before calling a proposal a decision, identify its source: confirmed invariant, authorized prior decision, measurement, or low-loss reversible choice. User preference alone establishes intent to examine the proposal, not that its implied components or mechanics are required.

When the request embeds a causal leap—`problem, therefore solution`—split it before proceeding:

```yaml
observed_problem: what is actually known
desired_outcome: behavior/state that should improve
proposed_mechanism: candidate named in the request
rival_explanations: causes for which that mechanism is ineffective or excessive
distinguishing_evidence: result that selects among mechanisms
```

If distinguishing evidence is absent, the next slice must collect it; do not implement the proposed mechanism, call it the initial choice, or design its internals. Example: when “report generation is slow, so make it asynchronous” lacks duration, deadline, workload, and user-behavior evidence, compare bottleneck optimization, interaction decoupling, and scheduled/precomputed delivery; do not yet define jobs, states, stores, workers, APIs, polling, retries, or notifications.

### 3. Find decision-reversing gaps

Scan the seven views below. Expand only a view whose answer could change the next slice or invalidate its design.

| View | Decision-reversing question |
|---|---|
| Outcome | Which behavior, decision, or state must change, and how would anyone observe it? |
| Context | What is inside, external, trusted, regulated, or owned elsewhere? |
| Scenario | Which normal, boundary, failure, recovery, and change path selects between options? |
| Data | What defines identity, validity, ownership, lifecycle, history, and conflict resolution? |
| Quality | Under what stimulus/environment must which artifact produce what measurable response? |
| Operation | Who detects, diagnoses, supports, restores, and authorizes degraded behavior? |
| Change | Which credible change is expensive to reverse, and which can be deferred behind telemetry? |

Use provisional design sketches to expose missing requirements; feed discovered constraints back into the requirement. Read [references/decision-framework.md](references/decision-framework.md) for routing, driver extraction, scenario construction, and reusable records.

### 4. Route each material unknown

| Unknown | Primary evidence | Decision artifact | Stop when |
|---|---|---|---|
| Meaning/term | Definition, positive/negative/boundary example | Semantic rule or example table | Cases classify consistently enough for the next slice |
| Domain rule/exception | Real case, operational record, accountable expert | Rule/decision table | Critical cases have one outcome and owner |
| Problem/value | Behavior observation, workflow evidence, prototype, limited release | Problem hypothesis and outcome measure | Evidence supports, rejects, or narrows the problem |
| Feasibility | Spike, benchmark, real data, walking skeleton | Capability result and constraint | Risky boundary meets/fails a stated test |
| Quality | Quality-attribute scenario and test | Measurable response | Threshold/bound is sourced or exposed as a decision |
| Conflict | Options, losses, governing constraint, authority | Decision record | Authorized owner accepts one loss profile |
| Future state | Change scenario, reversible boundary, telemetry, staged adoption | Revisit trigger | Current design preserves a cheap enough reversal |

If a retrievable fact changes the next action, ask or fetch only that fact. Otherwise observe, experiment, decide, or proceed reversibly. Use at most one blocking question; state non-blocking assumptions and continue.

### 5. Rank evidence by decision value

Prioritize qualitatively:

```text
priority ∝ loss_if_wrong × reversal_cost × uncertainty × decision_imminence
```

Prefer the cheapest evidence that distinguishes live options; do not assign pseudo-precise scores. Define the evidence packet:

```yaml
hypothesis: current best explanation
alternatives: materially different explanations or options
observation: evidence whose outcomes distinguish them
decision: choice or commitment that changes after the result
stop_rule: implement / investigate further / stop conditions
owner: authority for the resulting decision
```

### 6. Make design conditional until evidence selects it

When a missing driver can reverse the design:

1. Separate confirmed invariants from assumptions.
2. Compare at most two or three option families that differ on that driver.
3. For each option, name its selection condition, accepted loss, reversibility, and required evidence.
4. Select only when required by an invariant or when provisional use is low-loss and explicitly reversible.
5. Defer internal differences irrelevant to the next slice to the implementing team.

Do not turn a possible future channel, vendor, scale, or reuse case into a generic framework. Read [references/candidate-patterns.md](references/candidate-patterns.md) when examples are requested or one phrase admits multiple interpretations.

Apply a trace test to every concrete element:

```text
component / state / endpoint / store / retry / threshold
    <- required by which confirmed scenario, constraint, or measurement?
```

If no answer exists, delete it or demote it to a conditional option. When drivers remain unresolved, specify behavioral contracts and discriminating scenarios; do not fill the gap with a component diagram, API shape, state machine, data schema, or operational constant.

### 7. Define the smallest decision-producing E2E slice

Choose the smallest path that crosses the main uncertain boundary or distinguishes the live options:

```yaml
actor_entry: who initiates what
path: minimum real boundaries crossed
observable_result: user/system outcome
critical_failure: failure behavior demonstrated
evidence: measurement, trace, test, or observation produced
decision_unlocked: commitment enabled by the result
rollback: recovery if the assumption fails
```

A small code change that avoids the risky boundary is not a useful slice. Implement it only when the user authorized implementation; otherwise propose it.

An evidence slice may be instrumentation, observation, a throwaway benchmark, or a paper/prototype interaction. Do not force an E2E implementation slice when the mechanism itself has not passed the proposal-to-decision gate.

### 8. Shape 1–3-team or partner work around the boundary

Share only what dependencies require:

- responsibility for business rules, data, changes, decisions, incidents, and support;
- interface semantics, schema, authentication, versioning, errors, duplicate behavior, and timeout ownership;
- normal, duplicate, timeout, partial-failure, recovery, and compatibility scenarios;
- contract tests, representative data, sandbox/environment, and first E2E trace;
- release order, notice, compatibility window, rollback, and escalation path.

Keep each party's internal design private unless it changes the contract, operability, acceptance, or release dependency.

## Return decision-ready output

Use only populated sections:

```markdown
## Current frame
<provisional outcome, scope, facts, invariants>

## Decisions and drivers
| Status | Driver/unknown | Why it changes the design | Evidence or owner |

## Conditional design
| Option | Select when | Accepted loss | Reversal |

## Next evidence or slice
<action, observable result, decision unlocked, stop rule>

## Material assumptions and risks
<only items capable of reversing the recommendation>
```

Do not return a questionnaire, generic checklist, exhaustive diagram set, or architecture selected from an example.

Frontload the conclusion and decisive uncertainty. Prefer one compact driver/option table over separate inventories of requirements, functions, components, and tests that repeat the same decision. Add detail only when its deletion could change action, risk, or confidence.

## Completion gate

Revise once if any answer is no:

- Does every blocking question have an answer source and decision consequence?
- Are facts, assumptions, hypotheses, decisions, and unknowns distinguishable?
- Does every unresolved driver remain attached to conditional options rather than an invented default?
- If the request says “problem, therefore solution,” did the response separate them and avoid designing/implementing the solution until distinguishing evidence selects it?
- Does every concrete component, state, endpoint, store, retry policy, and threshold trace to a confirmed scenario/constraint/measurement? Otherwise remove or conditionalize it.
- Are numerical constants sourced, measured, or explicitly test variables?
- Does the next evidence cross the decisive uncertainty and have a stop rule?
- Is design detail sufficient for the next slice: actor/entry/result/failure, data and responsibility ownership, decisive quality test, integration proof, and rollback?
- For partner work, are shared contracts and owners explicit without demanding internal implementation?
- Would deleting any section change a choice, action, risk assessment, or confidence? If not, delete it.

Read [references/research-basis.md](references/research-basis.md) only for academic rationale or evidentiary limits. Distinguish reported findings from this skill's synthesis; do not claim universal productivity effects.
