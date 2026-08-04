---
name: gate-skill-candidates
description: Gate every proposal to create a new skill before anything is built: score recurrence, behavioral delta, trigger fitness, minimal mechanism, and context economy against the actual skill inventory, then route the candidate to skill, merge-into-existing-skill, reference-doc-only, no-build, or split. Use whenever the user proposes making something a skill, says skill化, asks whether an idea deserves a skill, or requests an inventory audit for keep, merge, demote, or delete. Do not use for editing an existing skill, building an already-admitted skill, or explaining how skills work.
---

# Gate skill candidates

Every admitted skill taxes every future session: its metadata is always loaded, and each addition makes description-based skill selection harder for the whole inventory. Admission is therefore default-deny, and the deliverable is a routing assignment—the cheapest mechanism that does the job—never a bare yes or no. Run the gate to completion before any skill authoring begins.

## Select the mode

| Request | Mode | Behavior |
|---|---|---|
| The user proposes a new skill, asks whether an idea deserves one, or presents a framework to turn into a skill | **Gate** | Score the five dials, emit the scorecard and routing table, hand admission artifacts to authoring |
| The user explicitly asks to review the existing skill inventory | **Audit** | Re-apply the dials to each named skill; verdict per skill: keep, merge, demote-to-reference, or delete |

A request to change, rename, or improve an existing skill is neither mode—make the edit without gating it. Do not enter audit mode implicitly.

## Gather in-context evidence

Identify the inventory the candidate would join, then read the actual frontmatter description of every skill in it before scoring any dial. Name the files read in the output. Rule from the inventory read this session, never from memory of what skills usually exist.

Do not score trigger fitness against remembered or assumed descriptions.
Do not rule on merge-into-existing-skill without quoting the target's actual description.

## Score the five dials

Every dial is pass/fail with a mandatory one-line evidence entry. An unevidenced pass is a fail.

| Dial | Pass question | Required evidence | On fail, route toward |
|---|---|---|---|
| Recurrence | Does this judgment or procedure recur across projects and sessions? | Two or more occasions that actually happened or are concretely foreseeable—not anticipated "someday" needs | no-build |
| Behavioral delta | Does Claude behave differently with the skill than without? | A named baseline failure: a specific gap observed (or reproduced this session) when Claude worked without the skill | no-build or reference-doc-only |
| Trigger fitness | Can a description be written that fires on the right moments and only those? | Both directions: (a) three or more concrete utterances that must NOT trigger it, distinct from every existing description; (b) firing moments complex enough that a model would consult a skill at all | merge-into-existing-skill or no-build |
| Minimal mechanism | Is a skill the cheapest sufficient mechanism? | Why an edit to an existing skill, a plain reference document, and doing nothing each fall short, cheapest first | the cheapest sufficient mechanism |
| Context economy | Does firing frequency × value-when-correct beat the standing metadata tax plus the selection externality on every existing skill? | A rough frequency estimate and the cost of a mis-fire | reference-doc-only or no-build |

Two failure modes end the evaluation early:

- **Unfalsifiable candidate.** If three concrete false-trigger utterances cannot be written, reject skillhood outright. An unfalsifiable description always over-fires.
- **Skill that would never fire.** Models consult skills only for work they cannot easily do alone; a simple one-step wish or an always-on rule of conduct will not trigger a skill however well the description matches. Such content cannot be delivered through the skill mechanism—route it toward merge or no-build and say why.

Do not soften a failed dial into a "partial pass".

## Assign the verdict

- **skill** — all five dials pass with evidence. Produce the admission artifacts below.
- **merge-into-existing-skill** — the capability belongs inside a neighbor. Name the target skill and the receiving section, and confirm the host's description still holds after absorption.
- **reference-doc-only** — knowledge worth keeping that changes no behavior. Name the file it becomes.
- **no-build** — a one-off prompt suffices, or the skill mechanism cannot deliver the behavior. Say so without apology.
- **split** — the candidate decomposes into parts with different fates. Gate each part independently and emit one routing row per part.

Split is an expected outcome, not an edge case: a candidate that mixes a recurring judgment procedure with short always-on rules of conduct typically splits, and the rules-of-conduct side then fails trigger fitness on its own.

Do not average dials into an overall score; the verdict is the routing that the failed dials force.

## Emit the routing table

Always emit both tables, per part when split:

```markdown
| Dial | Pass/Fail | Evidence |
|---|---|---|

| Part | Verdict | Destination | Deciding dial | Next action |
|---|---|---|---|---|
```

Destination is concrete: the target skill and section for merge, the file for reference-doc-only.

When any row's verdict is skill, add the three admission artifacts:

1. a draft description—third person, single line, stating what the skill does, when to use it with concrete trigger keywords, and what it must not be used for;
2. the three or more false-trigger utterances;
3. the nearest-neighbor skill in the inventory plus one boundary sentence separating them.

A skill verdict without all three artifacts is not a verdict; it is a hunch. Hand the artifacts to the authoring workflow. Do not build the admitted skill inside the gate.

## Handle audit mode

Apply the same five dials to each skill the user placed in scope, as if it were re-applying for admission. Use observed firing history from the conversation and repository when available. Emit the same two tables with retention verdicts: keep, merge (name the absorbing skill), demote-to-reference (name the file), or delete.

Do not edit or delete anything in audit mode.
Do not audit skills the user did not put in scope.

## Respect user override

When the user explicitly orders the build, comply immediately—the gate advises, the user decides. Record exactly one line in the output: `Gate note: would have routed to <verdict> (<deciding dial>). Built on user instruction.`

Do not block, re-argue, or require confirmation after an explicit build order.
Do not lecture about context economy when overridden.
Do not re-gate a candidate the user already overrode in this conversation.

## Keep the gate honest

Do not rubber-stamp: a run with five unexamined passes is gate theater; every pass needs its evidence entry.
Do not expand the output beyond the two tables and the admission artifacts.
Do not apply the gate when the user asks to edit, rename, or improve an existing skill.

Read [references/routing-mechanisms.md](references/routing-mechanisms.md) before writing any non-skill routing output. Read [references/worked-examples.md](references/worked-examples.md) when a verdict is contested or a candidate sits on a dial boundary. Read [references/research-basis.md](references/research-basis.md) only when the user challenges the gate's strictness or asks to tune a dial.

## Definition of done

- The target inventory's actual descriptions were read this session and named in the output.
- All five dials carry a pass/fail and a one-line evidence entry, per part when split.
- The verdict uses one of: skill, merge-into-existing-skill, reference-doc-only, no-build, split.
- Both tables are emitted; merge and reference verdicts name concrete destinations.
- Every skill verdict carries all three admission artifacts.
- An override carries the one-line gate note and nothing more.
- The gate built and edited nothing.
