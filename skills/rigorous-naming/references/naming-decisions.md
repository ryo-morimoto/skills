# Naming Decisions

Read this reference when emitting the final scannable report of terms the workflow adopted or re-checked, or when evaluating whether that report is too noisy or incomplete.

The report answers one question per term:

> Is this vocabulary choice acceptable to keep, or must it be reversed or escalated?

It is not a process diary, not a full candidate matrix, and not an audit inventory of every bad name in a file.

## When To Emit

Emit **Naming decisions** exactly when the [scope gate](../SKILL.md#apply-the-scope-gate) requires the full workflow for one or more terms in the task. That is the same threshold as skill fire for non-trivial naming.

Do not emit:

- when every touched name is exempt under the scope gate;
- for generated, vendored, prescribed, term-of-art, or tiny-scope locals;
- as a second prose restatement of the same rows.

In **verify** mode, emit the same fields for the terms in scope even when no file is edited. Add a **Status** column only in verify mode.

## Required Fields

| Field | Content | Omit when |
|---|---|---|
| **Id** | Short serial for pointing: `n1`, `n2`, … within this block only | never for a reported row |
| **Term** | Selected identifier or domain term | never for a reported row |
| **Definition** | One sentence: context + meaning + includes + excludes | never; if unwritable, stop and investigate instead of reporting |
| **Use site** | One representative call, access, type position, test name, error, or doc sentence | never; declaration-only is allowed only when no other use site exists yet, and must say so |
| **Rejected (why)** | One serious alternative and one concrete rejection reason | only when no genuine alternative existed (mechanical spelling of an already-canonical term is exempt, not reported) |
| **Surface** | `local` \| `shared` \| `public` | never |
| **Compat** | `n/a` for local/shared without external consumers; otherwise the strategy (`unchanged`, `alias`, `migrate`, `version`, or a short concrete plan) | use `n/a` rather than inventing ceremony |

### Id rules

- Format: `n` + decimal integer, no zero-padding (`n1`, `n2`, … `n10`). Easy to type in chat (`n2が微妙`).
- Assign **after** sort, starting at `n1` for each Naming decisions block.
- One block = one contiguous sequence. Do not reuse gaps; do not use UUID, file paths, or long prefixes (`ND-001` is too long).
- Humans and follow-ups refer to the Id, not only the term, when flagging discomfort.

Optional, only when true:

- **Design signal:** one line that the honest name still exposes mixed responsibility or a missing abstraction. Point to [design-signals.md](design-signals.md). Do not add an empty column. Prefer `Design signal (n2): …` so the Id stays the handle.

Sort rows: `public`, then `shared`, then `local`. Multiple terms → one table. One term → the same table or the compact card below.

## Default Shape: Batch Table

```markdown
## Naming decisions

| Id | Term | Definition | Use site | Rejected (why) | Surface | Compat |
|---|---|---|---|---|---|---|
| n1 | `ItemStock` | Quantity record for an `Item`; excludes physical item identity | `item.stock.available` | `Inventory` — conflicts with RECORE vocabulary | public | wire unchanged |
| n2 | `BasCase` | In store ops, a buyback case; includes active intake; excludes stock quantity (`ItemStock`) | `openBasCase(memberId)` | `Purchase` — non-domain synonym | shared | n/a |
```

### Verify mode shape

```markdown
## Naming decisions

| Id | Status | Term | Definition | Use site | Rejected (why) | Surface | Compat |
|---|---|---|---|---|---|---|---|
| n1 | RISK | `userId` | … | … | `accountId` — concepts not proven identical | public | migration missing |
| n2 | OK | `BasCase` | … | … | `Purchase` — non-domain synonym | shared | n/a |
```

Status values:

- **OK** — definition, use site, and surface risk are coherent.
- **RISK** — keep only with an explicit follow-up (usually compatibility or design).
- **REJECT** — reverse or replace; do not treat as adopted.

List **Needs decision** bullets only for RISK/REJECT rows that require a human call, keyed by Id (`n1: …`).

## Single-Term Card

Allowed when exactly one term is in scope:

```markdown
## Naming decisions

### n1 `ready-for-human`
- **Definition:** dispatchable human work *now* (named owner, action, exit evidence); excludes passive dependency waits.
- **Use site:** label applied only when start conditions are satisfied.
- **Rejected:** `human-attention-needed` — attracts non-actionable waits.
- **Surface:** shared
- **Compat:** n/a (label name kept; meaning narrowed)
```

## Ban From This Surface

Do not put these in the Naming decisions block:

- search logs, file lists, or “I grepped for…” narration;
- full multi-candidate matrices (those belong in working comparison via [calibration.md](calibration.md));
- more than one rejected alternative unless a second reject changes the decision;
- casing, formatting, or style commentary;
- restating every row in prose under the table;
- exempt names “for completeness.”

## Positive And Negative Fixtures

### Accept

```markdown
| Id | Term | Definition | Use site | Rejected (why) | Surface | Compat |
|---|---|---|---|---|---|---|
| n1 | `captureAuthorizedPayment` | In checkout, capture a previously authorized payment; includes capture of held funds; excludes authorize-only and refund | `payments.captureAuthorizedPayment(id)` | `processPayment` — hides precondition and outcome | shared | n/a |
```

### Reject as a report (too little)

```markdown
Selected `captureAuthorizedPayment` after comparing alternatives.
```

Missing Id, definition boundary, use site, surface, and reject reason.

### Reject as a report (too much)

A multi-paragraph methodology, every file path touched, three near-identical losers, and a style note about camelCase. The reader must mine the decision.

### Exempt — no row

- `i` in a three-line loop;
- framework `getServerSideProps` when the framework name is required;
- fixing `colour` → `color` to the repo’s already-canonical spelling with no meaning change.

## Relationship To Other Outputs

| Artifact | Job |
|---|---|
| Working candidate comparison ([calibration.md](calibration.md)) | Choose among close options during the procedure |
| **Naming decisions** (this file) | Let a human accept or reverse the chosen terms after the procedure |
| Audit findings ([SKILL.md](../SKILL.md) audit mode) | Inventory problematic existing names; not a list of adoptions |
| Design signals ([design-signals.md](design-signals.md)) | Structural follow-up when an honest name remains unstable |
