# Candidate Sets for Ambiguous Requests

## Use policy

Use these rows to widen hypotheses, never to select architecture. For each request: retain only plausible interpretations; add a local counterexample; name evidence that separates them; stop when the next evidence is unambiguous. The “premature commitment” column is explicitly a bad inference.

| Phrase | Materially different interpretations | Evidence that separates them | Decision produced | Premature commitment to avoid |
|---|---|---|---|---|
| “Make applications easier” | Fewer fields; less comprehension; fewer handoffs; lower wait/uncertainty; fewer corrections | Field/drop-off data, observed sessions, correction/support records, workflow timeline, prototype | Form, guidance, workflow, or status-feedback change | Redesigning the UI because “easy” sounds visual |
| “Make search faster” | Input feels slow; query latency; external dependency; result rendering; stale index; task takes too many searches | End-to-end traces, latency distribution by segment, query plan, dependency timing, task observation, freshness scenario | Optimize the measured segment or change interaction | Adding a DB index before locating latency/workload |
| “Real-time synchronization” | Human-immediate display; bounded propagation; read-after-write; conflict avoidance; event delivery; recovery after disconnect | Allowed delay, conflicting updates, outage/reconnect trace, freshness and loss scenarios | Consistency, conflict, transport, and recovery contract | Choosing streaming/event architecture from “real time” |
| “Support future extension” | Confirmed second variant; volatile vendor; credible scale step; policy change; unspecified anxiety | Change scenarios, frequency/history, coupling map, migration spike, telemetry | Boundary now, local implementation, or deliberate deferral | Generic plugin/adapter framework “just in case” |
| “Add notifications” | Reminder; state-change notice; action request; compliance evidence; operational alert | Event timeline, urgency, consent/preferences, duplicate and outage scenarios, observed follow-up behavior | Trigger, channel, delivery semantics, or no notification | Queue/worker/channel abstraction before delivery requirements |
| “We need an admin screen” | Frequent operational decision; rare correction; support lookup; bulk operation; audit/control requirement | Work observation, case frequency, role/authority matrix, mock-up, audit scenario | UI, scripted operation, report, workflow change, or no tool | CRUD screen for every entity |
| “Export CSV” | Human review; spreadsheet transformation; system import; audit snapshot; data portability | Downstream task observation, real sample, volume/encoding, access/retention, reproducibility scenario | Shape, delivery, snapshot semantics, or API/report alternative | One synchronous download with current rows |
| “Remove duplicate data” | Prevent duplicate creation; identify same entity; merge records; hide repeated display; preserve history | Collision cases, provenance, identity rules, merge/unmerge simulation, audit requirement | Validation, identity, merge, display, or history rule | Unique constraint or destructive merge before defining identity |
| “Make this an asynchronous job” | Avoid request timeout; free the UI; absorb bursts; schedule work; isolate failures; merely shorten a slow path | Current duration distribution, deadline, user behavior, workload peaks, failure/recovery scenario, dependency trace | Optimize current path, extend request, background execution, scheduling, or operational change | Queue, worker, job table, polling API, retries, and statuses before proving independent lifecycle |

## Basic-design diagnosis

| Observable symptom | Likely missing decision | Smallest discriminator | Sufficient output |
|---|---|---|---|
| Boxes/arrows exist but choices reopen | Critical scenario, driver, or accepted loss | Walk one decisive normal/failure/change scenario through boundaries | Conditional option + rationale + revisit trigger |
| API fields are known but integration feels risky | Semantics, state, timeout, duplicate, recovery, owner | Normal, duplicate, timeout-after-possible-acceptance, recovery traces | Contract test + responsibility boundary |
| Data-model debate loops | Identity, lifecycle, history, authority | Real create/correct/merge/delete/collision cases | Rule table + ownership + migration implication |
| Exception list expands indefinitely | Classification boundary or authority | Positive/negative/boundary cases, especially disputed one | Decision table + owner for residual disputes |
| Pattern debate has no winner | Missing comparative scenario/measure | Test options against one failure, quality, or change scenario | Select/reject conditions; defer if inconclusive |
| Partner questions expand into internals | Contract mixed with implementation autonomy | Mark each item shared only if it changes semantics, acceptance, operation, security, or release | Minimum shared contract; internal freedom elsewhere |
| Decision repeatedly reopens | Evidence, accepted loss, assumption, or invalidation trigger absent | Reconstruct the last fork and new evidence | Decision record with `revisit_when` |

## Worked transformations

### Ambiguous value: “Make the application form easier”

**Bad:** Ask the stakeholder to define every field, persona, exception, metric, and desired UI before proceeding.

**Decision-dense frame:**

```yaml
outcome: applicant completes a valid submission with less avoidable effort or uncertainty
hypotheses:
  - unnecessary fields cause abandonment
  - terms and validation cause correction loops
  - cross-team approval and waiting dominate perceived difficulty
  - lack of progress/status causes uncertainty despite acceptable completion time
evidence:
  observation: combine funnel/error data with 3–5 representative sessions and correction/support cases
  decision: choose form reduction, comprehension support, workflow change, or status feedback
  stop_rule: proceed when one cause explains a material observed failure; retain rivals if evidence is mixed
provisional_slice: one high-loss step from entry through valid submission and error recovery
```

The sample count is illustrative, not a universal threshold; use enough variation to expose the live fork.

### Unclear basic design: notifications with possible future SMS

**Bad:** Introduce a generic channel interface, queue, worker, retry table, and SMS adapter because SMS “may” arrive.

**Conditional design:**

| Option family | Select when | Reject/defer when | Evidence |
|---|---|---|---|
| Direct delivery from current use case | Failure may fail the use case; channels share consent/timing; change is cheap | Delivery must survive caller failure or channels differ materially | Failure and change scenarios |
| Decoupled delivery boundary | Business action and delivery have different availability/retry/latency semantics | No independent recovery or buffering requirement exists | Timeout/outage walking skeleton |
| Channel abstraction | A credible channel changes provider but preserves stable business semantics | SMS changes consent, urgency, payload, or guarantee so “same interface” hides differences | Concrete SMS change scenario |

Do not select retries, persistence, or timing constants until delivery guarantees and business tolerance supply them.

### Small partner integration: order API with unspecified retry ownership

**Bad:** Copy the API fields, assume synchronous success, choose retry counts, and request the partner's internal architecture.

**Decision-dense boundary:**

```yaml
decisive_scenario: caller times out after the partner may have accepted the order
shared_unknowns:
  - business identity and idempotency scope
  - accepted vs completed semantics
  - safe retry or prior-result lookup
  - reconciliation and incident owner
conditional_options:
  - retry only if duplicate safety is contractually testable
  - query prior outcome if correlation and status semantics exist
  - manual reconciliation if automation cost exceeds evidenced frequency/loss
first_proof: sample-data E2E covering normal, duplicate, timeout, and recovery with traceable outcome
stop_rule: integrate only after each path produces one owned business outcome; leave timeout/retry values unresolved until measured or contracted
```

### Performance request: “Search must be fast”

**Bad:** Convert the proposed DB index into the requirement.

**Decision-dense investigation:** trace user action to rendering; segment UI, network, application, database, dependency, and freshness cost; measure distributions under representative queries/data; choose an intervention only if it materially reduces the product-owned bound without violating freshness or write cost. An index remains one hypothesis alongside query shape, interaction, caching, dependency, and result-size changes.

### Proposed architecture: “Make the daily report an asynchronous job”

**Bad:** Confirm asynchronous execution, then invent `202`, job IDs, states, a job table, worker, queue, retry API, polling, notifications, and durability requirements before measuring the current path or business deadline.

**Decision-dense frame:**

```yaml
outcome: report is available by the business-owned deadline without blocking an unacceptable user workflow
facts: current duration distribution and acceptable deadline are unknown
hypotheses:
  - generation itself exceeds the deadline
  - generation meets the deadline but holding the interaction causes perceived failure
  - peak contention or one dependency produces the tail
options:
  - optimize the measured bottleneck when total completion time is the constraint
  - background execution when work must outlive the interaction or absorb bursts
  - schedule/precompute when the business need is predictable and freshness permits
evidence: trace duration by input/load/dependency; observe user wait/return behavior; obtain the business deadline
stop_rule: select a lifecycle only when evidence distinguishes completion-time, interaction, burst, or scheduling needs
```

Only after background execution is selected should job identity, durability, duplicate behavior, state visibility, cancellation, retry, retention, and notification be designed from scenarios. “Asynchronous” alone requires none of those specific mechanisms.

## Anti-overfitting checks

- If the example's named component disappeared, would the reasoning still work? If not, restate it as behavior, scenario, and trade-off.
- Did the example add a candidate or silently become “the architecture”? Restore at least one materially different option.
- Is a number sourced? If not, label it an experimental variable or remove it.
- Does local evidence select among candidates? If not, stop designing and define that evidence.
- Is the example rarer than the user's actual 1–3-team context? Remove scale-specific controls.
