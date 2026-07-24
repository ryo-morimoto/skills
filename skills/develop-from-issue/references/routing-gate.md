# Routing Gate: Condition Judgment and Decomposition

Use this reference during triage (phase 1) and when design (phase 2) emits a split. The gate exists to answer one question: **can this issue be implemented autonomously without deciding anything a human should own?** Route by which condition fails, because the failing condition names the work that comes next.

## Judging each condition

Gather evidence before judging: read the issue body and comments, inspect the code paths the issue names, and check for existing patterns, tests, and prior decisions. A condition judged without looking at the codebase is an assumption, not a verdict.

### 1. Requirement clear

**Passes:** the issue states an observable behavior change and the done criteria can be written down without asking anyone anything new.

- Pass: "`GET /users/:id` returns 404 with body `{error: "not_found"}` for a deleted user; today it returns 500." Behavior, trigger, and expected result are all present.
- Fail: "検索をもっと使いやすくしたい." Which behavior changes, for whom, observable how — all missing. The unknown is *meaning*: route `human` and resolve it with examples and questions per `clarify-requirements-and-design`, not by guessing.

A requirement that embeds a solution ("slow, so add an index") passes only if the *problem* behavior is also stated; otherwise the causal leap itself is the unknown.

### 2. Solution effectively single

**Passes:** an existing codebase convention covers the change, or the remaining alternatives differ only in ways that are cheap to reverse.

- Pass: adding a validation to a form where twelve other fields already follow one validation pattern.
- Fail: "add caching" where in-process, Redis, and HTTP caching all plausibly fit and differ in operations, invalidation, and infrastructure. The unknown is a *tradeoff*: it needs options, an accepted loss, and a decision owner.

Alternatives that differ materially in consequence — cost, failure mode, operability, lock-in — always fail this condition, even when one option "feels obvious."

### 3. Design-neutral

**Passes:** the change stays inside existing boundaries — no new or changed public interface, persisted schema, dependency, authorization boundary, or quality tradeoff.

- Pass: fixing an off-by-one inside one function; adding a field to an internal DTO no other team consumes.
- Fail: any new endpoint, event, table, column with meaning, third-party library, or a change that trades latency for consistency. These are commitments others will build on; commitments get a decision record.

### 4. Machine-verifiable

**Passes:** an automated test can demonstrate the done criteria.

- Pass: behavior reachable by unit/integration/E2E test in the existing harness.
- Fail: "the dashboard should feel faster" with no measurable threshold, or behavior only observable in a third-party sandbox that CI cannot reach. Either make it measurable first (a threshold turns feel into a test) or route `human` with an explicit manual verification plan.

### 5. Reversible

**Passes:** `git revert` alone restores prior behavior.

- Pass: pure code change behind existing interfaces.
- Fail: schema migrations, data backfills, published API changes, renamed exports other repos import, anything a consumer may have observed and depended on. Irreversibility raises the evidence bar; a human accepts that loss profile, not the workflow.

### Safety ceiling

Authentication, authorization, payments, data deletion, schema migration, cryptography: route `human` even at 5/5. The cost of a wrong autonomous change in these areas is not bounded by the diff size.

## Routing by failing condition

| Failing condition | Dominant unknown | Route | Design-phase activity |
|---|---|---|---|
| 1 Requirement clear | Meaning / value | human | Examples, stakeholder questions, observation — via `clarify-requirements-and-design` |
| 2 Solution single | Tradeoff | human | Option table with accepted loss; decision owner selects |
| 3 Design-neutral | Commitment | human | Decision record for the boundary being created |
| 4 Machine-verifiable | Observability | human | Define the measurement or the manual verification plan first |
| 5 Reversible | Loss profile | human | Stronger evidence, rollback plan, owner sign-off |
| Size / bundling only | None — just too much at once | split | Decompose below, re-triage each slice |

Conditions fail together often. Route on the dominant one, but record all failures in the triage record — they all become design-phase inputs.

## Decomposition patterns for `split`

Split only when the issue bundles separable outcomes and the unknowns are *not shared*. If one design decision spans all the slices, decide first (route `human`), then split.

Every sub-issue must state its own observable behavior and done criteria, deliver value or evidence on its own, and be independently mergeable and verifiable — then it re-enters triage on its own merits.

| Pattern | Split by | Example |
|---|---|---|
| Vertical slice | One user-visible path end to end, thinnest first | "CSV import" → slice 1: single-row happy path; slice 2: validation errors; slice 3: 10k-row performance |
| Workflow step | Steps in a user or system workflow | "Approval flow" → submit / approve / notify, each observable alone |
| Rule variation | Business-rule cases | Base rate first; regional exceptions as later slices |
| Defer the rare case | Frequency | Happy path now; concurrent-edit conflict handling as its own issue |
| Spike, then build | Unknown vs known | Slice 1 is a timeboxed evidence slice answering the feasibility question, with a stop rule; the build slices are created only after it lands |
| Interface, then implementations | Contract vs consumers | Slice 1 lands the agreed contract plus a stub; consumer and provider proceed in parallel |

The first slice should cross the riskiest boundary, not the easiest one — a slice that avoids the uncertain part produces no decision.

## Split anti-patterns

- **Layer split** — "DB issue + API issue + UI issue." No slice is observable alone; nothing can be accepted until everything merges.
- **Artifact split** — "implementation issue + tests issue + docs issue." Tests are part of done criteria, not a sibling deliverable.
- **Shared-unknown split** — slices that all depend on one undecided design. Decide once at the parent, then split.
- **Deep nesting** — sub-issues of sub-issues. One decomposition level; if a slice still fails the gate, it routes `human`, not `split` again.
- **Forced split** — decomposing to make work look autonomous. A slice that cannot state its own done criteria was not a slice.

## Stop rule

After one honest decomposition attempt, every slice either passes the gate (`auto`) or has a named failing condition (`human`). If most slices still route `human`, the issue's real problem is upstream — undecided requirements or design — and the parent goes to `stage:design` instead of `stage:tracking`.
