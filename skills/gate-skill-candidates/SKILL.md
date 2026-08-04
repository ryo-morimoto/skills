---
name: gate-skill-candidates
description: Gate skill creation at the moment of build intent: before building any proposed skill, score recurrence, behavioral delta, trigger fitness, minimal mechanism, and context economy against the actual skill inventory, then route the candidate to skill, merge-into-existing-skill, project-memory, reference-doc-only, no-build, or split. Use whenever the user asks to build a skill, says skill化, asks whether an idea deserves one, or requests an inventory audit. Answer advisory questions with a compact verdict, not the full audit format. Do not use for editing an existing skill or explaining how skills work.
---

# Gate skill candidates

Every admitted skill taxes every future session: its metadata is always loaded, and each addition makes description-based skill selection harder for the whole inventory. Admission is therefore default-deny, and the deliverable is a routing assignment—the cheapest mechanism that does the job—never a bare yes or no. The gate's value concentrates at build moments: an ungated assistant builds whatever it is told to build. Advisory questions deserve the same judgment in far fewer words—blind evaluation showed process scaffolding costs more than it earns there (see references/research-basis.md).

## Select the mode

| Request | Mode | Behavior |
|---|---|---|
| The user orders a skill built—"スキルにして", "make this a skill", content presented for building | **Gate-and-build** | Score the dials before touching a file; a skill verdict proceeds to authoring with the admission artifacts; any other verdict delivers the routed alternative, drafted |
| The user asks whether something deserves a skill | **Advisory** | Run the same dials internally; reply with the compact verdict only |
| The user explicitly asks to review the existing skill inventory | **Audit** | Re-apply the dials to each named skill; verdict per skill: keep, merge, demote-to-reference, or delete; full format |

A request to change, rename, or improve an existing skill is none of these—make the edit without gating it. Do not enter audit mode implicitly.

## Gather in-context evidence

Identify the inventory the candidate would join, then read the actual frontmatter description of every skill in it before scoring any dial. Rule from the inventory read this session, never from memory of what skills usually exist.

Do not score trigger fitness against remembered or assumed descriptions.
Do not rule on merge-into-existing-skill without quoting the target's actual description.
Do not narrate the inventory reading in a compact reply; cite only the description that grounds the verdict.

## Score the five dials

Every dial is pass/fail with a mandatory one-line evidence entry. An unevidenced pass is a fail.

| Dial | Pass question | Required evidence | On fail, route toward |
|---|---|---|---|
| Recurrence | Does this judgment or procedure recur across projects and sessions? | Two or more occasions that actually happened or are concretely foreseeable—not anticipated "someday" needs | no-build |
| Behavioral delta | Does Claude behave differently with the skill than without? | A named baseline failure: a specific gap observed (or reproduced this session) when Claude worked without the skill | no-build or reference-doc-only |
| Trigger fitness | Can a description be written that fires on the right moments and only those? | Both directions: (a) three or more concrete utterances that must NOT trigger it, distinct from every existing description; (b) firing moments complex enough that a model would consult a skill at all | merge-into-existing-skill or project-memory |
| Minimal mechanism | Is a skill the cheapest sufficient mechanism? | Why project-memory lines, an edit to an existing skill, a plain reference document, and doing nothing each fall short, cheapest first | the cheapest sufficient mechanism |
| Context economy | Does firing frequency × value-when-correct beat the standing metadata tax plus the selection externality on every existing skill? | A rough frequency estimate and the cost of a mis-fire | reference-doc-only or no-build |

Two failure modes end the evaluation early:

- **Unfalsifiable candidate.** Attempt the three false-trigger utterances visibly—write the actual utterances, or the explicit argument that every ordinary request would trigger the skill. An unstated attempt does not count. If three cannot be produced, reject skillhood outright: an unfalsifiable description always over-fires. An unfalsifiable rule stays unfalsifiable in project-memory or anywhere else—do not draft it into memory lines; route to no-build unless a falsifiable reformulation exists, and draft that reformulation instead.
- **Skill that would never fire.** Models consult skills only for work they cannot easily do alone; a simple one-step wish or an always-on rule of conduct will not trigger a skill however well the description matches. Route such content to project-memory (guaranteed ambient application) or merge, and say why.

Do not soften a failed dial into a "partial pass".

## Assign the verdict

- **skill** — all five dials pass with evidence. Produce the admission artifacts below.
- **merge-into-existing-skill** — the capability belongs inside a neighbor. Name the target skill and the receiving section, and confirm the host's description still holds after absorption.
- **project-memory** — always-on conduct or short constant rules. Draft the actual lines (three or fewer, imperative) for the target environment's always-loaded instruction file (CLAUDE.md, AGENTS.md, or equivalent).
- **reference-doc-only** — knowledge worth keeping that changes no behavior. Name the file it becomes.
- **no-build** — a one-off prompt suffices. Say so without apology.
- **split** — the candidate decomposes into parts with different fates. Gate each part independently, one verdict per part.

Split is an expected outcome, not an edge case: a candidate that mixes a recurring judgment procedure with always-on rules of conduct typically splits—procedure toward skill, rules toward project-memory.

Do not average dials into an overall score; the verdict is the routing that the failed dials force.

## Deliver the outcome

Two reply shapes. Pick by how much scoring actually happened, not by ceremony.

**Compact verdict** — for advisory questions and any early-exit rejection. Three elements in plain prose, nothing more: the verdict; the deciding evidence in one or two sentences; the concrete next action with its content already drafted (the memory lines, the merge destination, the reframed candidate). State the verdict decisively: when a part is skill-viable, say so outright—do not hedge an admission into "maybe later". No dial scorecard, no routing table, no inventory narration, no framework vocabulary beyond the verdict. Match the length of a direct expert answer.

**Full format** — for build orders that reach full five-dial scoring, audit mode, a contested verdict, or when the user asks to see the working. Emit both tables, per part when split:

```markdown
| Dial | Pass/Fail | Evidence |
|---|---|---|

| Part | Verdict | Destination | Deciding dial | Next action |
|---|---|---|---|---|
```

When any verdict is skill, add the three admission artifacts:

1. a draft description—third person, single line, stating what the skill does, when to use it with concrete trigger keywords, and what it must not be used for;
2. the three or more false-trigger utterances;
3. the nearest-neighbor skill in the inventory plus one boundary sentence separating them.

A skill verdict without all three artifacts is not a verdict; it is a hunch.

On a build order: a skill verdict proceeds to authoring with the artifacts applied. Any other verdict delivers the routed alternative drafted and ready to use; build the skill anyway only on explicit insistence, recording the gate note below.

## Handle audit mode

Apply the same five dials to each skill the user placed in scope, as if it were re-applying for admission. Use observed firing history from the conversation and repository when available. Emit the full format with retention verdicts: keep, merge (name the absorbing skill), demote-to-reference (name the file), or delete.

Do not edit or delete anything in audit mode.
Do not audit skills the user did not put in scope.

## Respect user override

When the user explicitly insists on the build against a non-skill verdict, comply immediately—the gate advises, the user decides. Record exactly one line in the output: `Gate note: would have routed to <verdict> (<deciding dial>). Built on user instruction.`

Do not block, re-argue, or require confirmation after an explicit build order.
Do not lecture about context economy when overridden.
Do not re-gate a candidate the user already overrode in this conversation.

## Keep the gate honest

Do not rubber-stamp: a run with five unexamined passes is gate theater; every pass needs its evidence entry.
Do not pad a compact verdict with process scaffolding; this gate's blind-tested failure mode is bloat, not leniency.
Do not apply the gate when the user asks to edit, rename, or improve an existing skill.

Read [references/routing-mechanisms.md](references/routing-mechanisms.md) before drafting any non-skill routing output. Read [references/worked-examples.md](references/worked-examples.md) when a verdict is contested or a candidate sits on a dial boundary. Read [references/research-basis.md](references/research-basis.md) only when the user challenges the gate's strictness or asks to tune a dial.

## Definition of done

- The target inventory's actual descriptions were read this session (named in full-format output only).
- All five dials carry a pass/fail and evidence, or a named early exit ended the run.
- The verdict uses one of: skill, merge-into-existing-skill, project-memory, reference-doc-only, no-build, split.
- Compact replies contain the verdict, the deciding evidence, and a drafted next action—and no tables.
- Full format carries both tables; every skill verdict carries all three admission artifacts.
- Non-skill verdicts name concrete destinations with their content drafted.
- An override carries the one-line gate note and nothing more.
- Nothing was edited or deleted in audit mode.
