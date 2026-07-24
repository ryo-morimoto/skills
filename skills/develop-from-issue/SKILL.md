---
name: develop-from-issue
description: Drive a GitHub issue through the full development loop — triage requirements, route to automatic implementation, human-led design, or decomposition into sub-issues, then implement, verify, merge, and run acceptance. Use when asked to progress, triage, or resume an issue, judge a verification result, or run issue-driven development end to end. Operates GitHub Issues exclusively via gh api graphql and persists all workflow state on the issue itself. Do not use for code changes without a backing issue, for standalone requirements or design consulting (use clarify-requirements-and-design), or for repositories whose issues must not be modified.
---

# Develop from Issue

Drive one GitHub issue through `triage → (auto | design | split) → implement → verify → (merge → acceptance | discard → feedback)`. All workflow state lives on the issue as labels and marked comments; every run reads the live state, executes exactly the current phase, and stops at human gates.

## Non-negotiable controls

| Control | Required behavior | Failure prevented |
|---|---|---|
| Issue is the single source of state | Read stage label and latest marked record comments before acting; never infer phase from conversation memory | Divergent state, duplicated or skipped work |
| Route by dominant uncertainty, not size | Route `auto` only when every upstream gate condition passes with cited evidence; a failing condition names the next activity | Autonomous implementation of undecided work |
| Design effort proportional to risk | Spend design only where a wrong choice is expensive to reverse; skip ceremony where it is not | Ceremony on trivial work; naked commitment on risky work |
| Verification ≠ validation | Merge on verification (built right); close the issue only on acceptance (right thing) | "Merged" mistaken for "done" |
| PR is a probe, not sunk cost | When failure invalidates the decision — or after two bounded repair rounds — close the PR unmerged and feed the learning upstream | Patch loops that bury a wrong design |
| Diff traces to the record | Every change in the PR traces to the recorded requirement or decision; out-of-scope discoveries become new issues | Scope creep, unreviewable diffs |
| Human owns irreversible and tradeoff points | Stop and wait at design approval and at acceptance; merge autonomously only on auto-routed issues that passed verification | Automation past authority |
| Issue writes via `gh api graphql` with variables | Pass bodies through files and GraphQL variables, never shell-interpolated query strings; read every write back to verify | Injection, silent write failure |

## State model

Stage labels — exactly one on an open workflow issue:

| Label | Meaning | Exit |
|---|---|---|
| `stage:triage` | Awaiting routing | Triage record posted |
| `stage:design` | Human-led requirement/design work | Decision owner approves |
| `stage:ready` | Decision recorded, implementable | Implementation starts |
| `stage:implementing` | Branch open, work in progress | PR opened |
| `stage:verify` | PR open, awaiting verdict | Merge or discard |
| `stage:acceptance` | Merged, awaiting validation | Accept or reject |
| `stage:tracking` | Split parent; children carry the work | All sub-issues accepted |

Marked record comments — the latest comment starting with each marker is the current record:

`<!-- idd:triage -->` routing record · `<!-- idd:decision -->` decision record · `<!-- idd:verdict -->` verification verdict · `<!-- idd:feedback -->` upstream feedback · `<!-- idd:acceptance -->` acceptance request/result

Recipes for every read, write, label setup, and fallback: [references/github-graphql-operations.md](references/github-graphql-operations.md). If the stage labels do not exist in the repository, run the one-time setup first.

## Execute the workflow

### 0. Locate state

Fetch the issue: labels, body, marked comments, sub-issues, parent. No stage label → start at triage. Otherwise execute only the phase the label names. Never skip ahead, and never re-run a phase whose record already answers the question at hand.

### 1. Triage — the upstream gate

Route `auto` only if all five conditions hold, each backed by evidence from the issue text or the codebase — not by optimism:

| # | Condition | Passes when |
|---|---|---|
| 1 | Requirement clear | Expected behavior is observable and done criteria are derivable from the issue without new stakeholder input |
| 2 | Solution effectively single | An existing codebase pattern covers it; remaining alternatives do not differ in material consequence |
| 3 | Design-neutral | No new or changed public interface, schema, dependency, authorization boundary, or quality tradeoff |
| 4 | Machine-verifiable | An automated test can demonstrate the done criteria |
| 5 | Reversible | Plain `git revert` restores prior behavior; no migration or external contract change |

Safety ceiling: even at 5/5, route `human` when the change touches authentication, authorization, payments, data deletion, schema migration, or cryptography.

Outcomes:

- **auto** — post the triage record, label `stage:ready`, continue to phase 3 in the same run.
- **split** — the issue fails only by bundling separable outcomes: decompose per [references/routing-gate.md](references/routing-gate.md), create sub-issues each stating observable behavior and done criteria, attach them with `addSubIssue`, label the parent `stage:tracking`. Each sub-issue enters triage independently. One decomposition level; if slices still fail the gate, route them `human` — do not force splits.
- **human** — any other failing condition: label `stage:design`, record which conditions failed (they define the design work), go to phase 2.

```markdown
<!-- idd:triage -->
## Triage
route: auto | split | human
| # | condition | verdict | evidence |
failing condition → planned activity
```

### 2. Design — human-led

Run the failing conditions through `clarify-requirements-and-design`: separate facts from assumptions, route each unknown to its cheapest evidence, keep design conditional until evidence selects it. Post the outcome as a decision record, then stop and wait for the decision owner. Do not begin implementation while the decision is pending.

```markdown
<!-- idd:decision -->
## Decision record
context: <requirement and constraint facts>
| option | select when | accepted loss | reversal |
decision: <chosen option> — decided by <owner>
done criteria: <observable, testable>
revisit trigger: <evidence that reopens this decision>
```

Owner approval (comment or explicit confirmation) → relabel `stage:ready` and continue to phase 3. If design work reveals the issue bundles separable slices, route `split` from here instead.

### 3. Implement

Preconditions: `stage:ready` plus a triage record (auto) or approved decision record (human).

- Branch `issue-<number>-<slug>`; label `stage:implementing`.
- Implement only what the record states; write the automated test that demonstrates the done criteria.
- Out-of-scope discovery → create a new issue at `stage:triage`; do not widen the diff.
- Open a PR referencing the issue **without closing keywords** (`Refs #N`, not `Closes #N`) — issue closure belongs to acceptance, not merge. Label `stage:verify`.

### 4. Verify — the downstream gate

Verification = build + full test suite + lint/typecheck + self-review of the diff against the record, plus CI and human review where the repository requires them.

- **Pass** → post the verdict, merge the PR (auto-routed: merge directly; human-routed: follow the repository's review rules), relabel `stage:acceptance`, go to phase 5.
- **Fail, execution-level** — defect local to the code while the recorded decision still holds: repair in the PR. At most two repair rounds; a third failure is decision-level by definition.
- **Fail, decision-level** — approach unworkable, requirement misread, unforeseen constraint, diff no longer traces to the record, or repair budget exhausted: close the PR unmerged, keep the branch as evidence, post the feedback record, relabel `stage:design` (decision was wrong) or `stage:triage` (requirement was wrong), and stop for the human.

```markdown
<!-- idd:verdict -->
## Verification
build / tests / lint: <results>
diff ⇔ record trace: <holds / broken where>
verdict: merge | repair (round n/2) | discard
```

```markdown
<!-- idd:feedback -->
## Upstream feedback
failed at: <observable failure and evidence>
invalidates: requirement | solution choice | design decision — <which one>
learned: <constraint or fact discovered by the attempt>
discarded PR: #<pr> (branch kept as evidence)
re-entry: <stage and what must change before retrying>
```

### 5. Acceptance — validation

After merge, post the acceptance request — what changed, how to observe it, the done criteria to check — mentioning the requester, then stop.

- **Accepted** → close the issue with `closeIssue` and `stateReason: COMPLETED`. A `stage:tracking` parent closes when all sub-issues are accepted.
- **Rejected** → a validation gap is a requirement or value problem, not an execution defect: post the feedback record, relabel `stage:triage`, and start a new cycle through the gate. Never fix forward without re-entering triage.

## Skill composition

This skill only sequences and gates; phase methods belong to their own skills:

- `clarify-requirements-and-design` owns phase 2 (and any triage where requirement meaning itself is the unknown).
- `orient` runs silently before any question to a human, in any phase.
- `distill-decision-signal` compresses long investigation output into record comments.

Record comments are the interface between phases: any phase skill can be replaced as long as it reads and writes the same records.

## Completion gate

Revise the run if any answer is no:

- Did the run read live issue state first and execute only the current phase?
- Is every state change written back (label + record comment) and verified by reading it back?
- On `auto`: does each of the five conditions cite evidence rather than assumption?
- Was every question to a human attached to a decision it could change?
- On failure: does the feedback record name what was invalidated and what was learned — not just that tests failed?
- Did the run stop at the correct human gate instead of continuing past authority?

Read [references/routing-gate.md](references/routing-gate.md) for condition-level judgment and decomposition patterns, and [references/research-basis.md](references/research-basis.md) only for the evidence behind this workflow and its limits.
