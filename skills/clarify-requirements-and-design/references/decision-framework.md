# Decision Framework

## Contents

- [Uncertainty routing](#uncertainty-routing)
- [Question economics](#question-economics)
- [Design-driver extraction](#design-driver-extraction)
- [Conditional option selection](#conditional-option-selection)
- [Quality-attribute scenarios](#quality-attribute-scenarios)
- [Small cross-boundary design](#small-cross-boundary-design)
- [Reusable records](#reusable-records)

## Uncertainty routing

Stop triage when one safe next action and its stopping condition are known.

| Unknown type | Diagnostic | Best first evidence | Weak substitute | Output | Stop condition |
|---|---|---|---|---|---|
| Semantic | People use the same word for different cases | Positive, negative, boundary examples; operational definition | More polished wording | Classification rule | Relevant cases classify consistently |
| Domain | Correct outcome depends on business facts/exceptions | Recent real cases; rule source; accountable expert | Generic brainstorming | Decision/rule table | Critical cases have outcome, rationale, owner |
| Problem/value | Nobody knows whether behavior or outcome improves | Observation, workflow evidence, prototype, limited release | Stakeholder preference alone | Problem hypothesis + outcome measure | Hypothesis supported, rejected, or narrowed |
| Feasibility | Capability at a risky boundary is unknown | Spike, benchmark, real data, walking skeleton | Architecture debate | Measured constraint | Test passes/fails under stated conditions |
| Quality | “Fast”, “secure”, “reliable” lacks operating conditions | Quality scenario + measurement | Adjective or universal best practice | Source/stimulus/environment/response/measure | Bound is agreed or exposed as owner decision |
| Conflict | Valid interests imply different losses | Option/loss comparison + decision authority | More discovery without authority | Decision record | Owner accepts one loss profile |
| Future | Change or scale is plausible but unverified | Change scenario, telemetry, staged adoption | Framework “just in case” | Revisit trigger + reversible boundary | Reversal cost is acceptable and observable |

Escalate first when safety, law, security, irreversible data loss, or contractual commitment is involved. Establish the constraint, evidence threshold, and accountable owner before implementation.

### Minimal routing algorithm

```text
known record/person + answer changes action -> retrieve/ask one fact
unknown value/problem                         -> observe or prototype
unknown feasibility                           -> experiment at risky boundary
underspecified quality                        -> scenario + measure
conflicting interests                         -> compare losses + decide
uncertain future                              -> reversible choice + telemetry
otherwise                                     -> record assumption + proceed + rollback
```

## Question economics

A blocking question is justified only when all four hold:

1. an answer exists now;
2. a known person or record can supply it;
3. plausible answers select different next actions;
4. interruption and delay cost less than proceeding reversibly or collecting direct evidence.

Write it as:

```text
Decision: <what will change>
Fork: if <A>, do <X>; if <B>, do <Y>
Ask: <one retrievable fact>
Source: <person or record>
```

| Low-density question | Decision-bearing replacement |
|---|---|
| What are all exception cases? | Show one accepted, one rejected, and one disputed case; who owns the disputed outcome? |
| How fast must it be? | Which user/system action fails if p95 exceeds which observed or contractual bound, under what load? |
| Should this support future channels? | Which credible channel differs in payload, consent, delivery guarantee, or failure handling enough to change today's boundary? |
| What happens on error? | For timeout after possible acceptance, may we retry, query prior outcome, compensate, or require manual reconciliation? |

Keep other gaps as explicit assumptions; do not serialize all unknowns into questions.

## Design-driver extraction

A fact is a design driver only if changing it can alter a boundary, data model, interface, technology, rollout, or operating model.

| Driver | Evidence with highest local value | Design forks it can select | Cost of guessing |
|---|---|---|---|
| Actor/outcome | Current workflow, observed decision, failure cost | Interaction and scope boundary | Correct feature, wrong problem |
| Domain invariant | Accepted/rejected/boundary cases; policy | Validation location, state transition, authority | Silent rule violations |
| Data identity/lifecycle | Real collisions, corrections, deletes, provenance | Keys, merge, history, source of truth | Corruption and irreconcilable records |
| Consistency | Conflicting update and stale-read scenarios | Transaction, reconciliation, concurrency rule | Duplicate/lost/conflicting outcomes |
| Dependency | Contract, owner, failure/change history | Coupling, fallback, release ordering | Integration and operational deadlock |
| Volume/latency/freshness | Distributions and peaks, not averages | Query/index/cache/async candidates | Premature optimization or missed SLO |
| Security/privacy | Threat, role, trust, retention, residency | Trust boundary, authorization, encryption, audit | Breach or compliance failure |
| Availability/recovery | Failure modes, business tolerance, RTO/RPO source | Degraded mode, redundancy, retry/recovery | Cascades or unrecoverable outage |
| Modifiability | Credible change scenario and frequency | Module/interface boundary, deferral | Speculative abstraction or costly change |
| Operability | Detection, diagnosis, support, restore owner | Telemetry, runbook, control surface | Unowned production failure |
| Delivery | Release dependency, migration, compatibility window | Flag, dual-read/write, migration, rollback | Blocked or irreversible release |

### Driver sufficiency

Proceed with the next slice when its actor, entry, result, and critical failure are known; data and responsibility ownership are explicit; one decisive quality scenario is testable; live options have selection conditions; and integration plus rollback can be demonstrated. This proves slice readiness, not whole-system completeness.

## Conditional option selection

Compare no more than three option families; omit internal variants that do not affect the next decision.

| Evidence state | Action |
|---|---|
| Confirmed invariant permits only one option | Select it; cite the invariant |
| One option is low-loss and cheap to reverse | Use provisionally; instrument and define rollback |
| Options create materially different irreversible loss | Defer; collect distinguishing evidence |
| Difference is internal and does not affect contract/slice | Delegate to implementing team |

For each live option record:

```yaml
option: behavior/boundary, not product slogan
select_when: scenario or fact favoring it
reject_when: scenario or fact invalidating it
accepted_loss: what becomes worse or impossible
reversal: migration/rollback path and cost
evidence: cheapest discriminator
```

Reject an option statement that merely names `queue`, `event-driven`, `adapter`, `microservice`, `cache`, or `table`; it lacks the scenario and loss that justify the boundary.

### Proposal-to-decision gate

Treat a solution named by the user, ticket, or stakeholder as a candidate unless one of these is explicit:

- an authorized prior decision makes it binding;
- a contractual, legal, safety, compatibility, or platform invariant requires it;
- current evidence rules out materially different option families;
- it is a deliberately provisional, low-loss choice with observable rollback.

Trace every concrete design element backward:

| Element proposed | Evidence required before commitment |
|---|---|
| Independent job lifecycle | Work must outlive interaction, absorb bursts, be scheduled, or isolate failure |
| Durable state | A scenario requires survival/recovery across process or dependency failure |
| Queue/broker | Measured buffering, delivery, ordering, isolation, or scaling need |
| Retry | Transient failure classification plus duplicate/side-effect safety |
| Polling/notification | Observed return behavior and freshness/urgency requirement |
| Adapter/extension point | Credible change differs behind a stable semantic boundary |
| Cache/index | Located latency/workload plus acceptable freshness/write trade-off |

If evidence is absent, describe the behavior to learn and the options it separates; do not manufacture the implementation implied by the label.

## Quality-attribute scenarios

Replace quality adjectives with six fields:

```yaml
source: entity generating the stimulus
stimulus: event affecting the system
environment: normal, peak, degraded, maintenance, attack, migration
artifact: affected system/interface/data/operation
response: observable required behavior
response_measure: threshold, bound, or explicitly unresolved test variable
```

| Attribute | Dense scenario | Design question unlocked |
|---|---|---|
| Performance | Peak-hour applicant submits a valid form; under measured peak concurrency, confirmation appears within the product-owned bound and no accepted submission is lost. | Optimize UI, request path, dependency, or background completion? |
| Availability | Partner times out after possibly accepting an order; ingestion returns or recovers one traceable business outcome without duplicate order creation. | Retry, status lookup, idempotency, compensation, or manual recovery? |
| Security | Support operator requests a restricted record during normal support; only authorized fields are shown and access is attributable under retention policy. | Where are authorization, redaction, and audit boundaries? |
| Modifiability | A confirmed second notification channel changes consent and delivery guarantees; add it without altering unrelated business-state transitions or existing channel behavior. | Is a channel boundary justified now, or only after the change is real? |
| Recoverability | Deployment corrupts newly written records before detection; restore service and reconcile affected records within business-owned RTO/RPO. | Backup, rollback, audit history, or dual operation? |

Numbers must come from contracts, user/business tolerance, observed distributions, or an explicitly labeled experiment. Never manufacture a threshold to complete the scenario.

## Small cross-boundary design

For 1–3 teams or one partner, coordinate the dependency, not the organizations.

| Shared control | Minimum decision content | Executable proof |
|---|---|---|
| Context | Systems, actors, trust and responsibility boundaries | One E2E trace across every owned boundary |
| Ownership | Rule, data, change, incident, support, decision owners | Named escalation and acceptance authority |
| Semantics | Meaning, state transitions, duplicate/out-of-order behavior | Positive, boundary, duplicate examples |
| Protocol | Schema, auth, version, errors, timeout ownership | Consumer/contract test against sample or sandbox |
| Failure/recovery | Partial acceptance, retry permission, reconciliation, degraded mode | Timeout and recovery exercise |
| Change | Notice, compatibility, release order, rollback | Compatibility test plus rollback rehearsal |

Do not request another party's class diagrams, internal task plan, or tooling unless it changes the contract, acceptance, operability, security, or release dependency.

### Interface contract semantics

Do not stop at field names. Resolve only the applicable semantic forks:

- identity, uniqueness, correlation, ordering, and deduplication;
- validity, units, timezone, null/absence, default, and unknown value;
- accepted vs completed, partial acceptance, and state transition authority;
- retry safety, prior-outcome lookup, timeout ownership, and reconciliation;
- authentication principal, authorization decision point, audit, retention;
- version compatibility, deprecation, notice, release order, rollback;
- rate/size bounds and the owner of operational changes.

## Reusable records

### Decision-ready work item

```yaml
outcome: observable actor behavior/state change
scope: inside, outside, externally owned
facts: verified constraints with source
assumptions: unconfirmed facts used to proceed
hypotheses: explanations/options awaiting evidence
scenarios: decisive normal, boundary, failure, recovery, change paths
drivers: facts capable of reversing design
options: select/reject conditions, accepted loss, reversal
evidence: hypothesis, observation, decision, stop rule, owner
slice: actor, real path, result, critical failure, proof
integration: contract, data/environment, release order
rollback: recovery if assumptions fail
decisions: selected option, rationale, revisit trigger, owner
```

### Architecture decision

```yaml
decision: selected behavior/boundary
status: proposed | accepted | superseded
drivers: governing scenarios and constraints
options: materially different alternatives
evidence: confirmed facts, measurement, prototype
accepted_losses: costs and foreclosed outcomes
assumptions: unconfirmed dependencies
consequences: implementation, operation, partner effects
revisit_when: observable invalidation condition
owner: accountable authority
```

### Evidence packet

```yaml
hypothesis: claim under test
alternatives: rival explanations
method: observation/prototype/spike/benchmark/slice
sample_conditions: data, environment, load, actors
observation: result that discriminates alternatives
decision: commitment changed by result
stop_rule: pass, fail, inconclusive actions
validity_risk: reason evidence may not generalize
owner: decision authority
```
