# Worked examples

Read this file when a verdict is contested, a candidate sits on a dial boundary, or you need to demonstrate the split verdict. Both examples are real gate runs, shown in the required output shape.

## Example 1 — this gate, under its own dials (clean admission)

Candidate: "a review gate that decides whether a proposed idea should become a skill".

| Dial | Pass/Fail | Evidence |
|---|---|---|
| Recurrence | Pass | "Make this a skill" requests recur in any maintained skill collection; this repository saw one in the very session that produced the gate |
| Behavioral delta | Pass | Baseline failure observed: asked to skill-ify a framework, the assistant eagerly planned a full skill without questioning admission at all |
| Trigger fitness | Pass | False triggers: "improve this skill's description", "fix this bug", "how does skill-creator work"; firing moments (admission judgment against an inventory) are multi-step |
| Minimal mechanism | Pass | An existing-skill edit has no host covering admission; a reference doc changes no behavior at proposal time; doing nothing repeats the ad-hoc debate each time |
| Context economy | Pass | Fires rarely (only on skill proposals), and each correct fire prevents a permanent metadata tax—value per fire is structurally high |

| Part | Verdict | Destination | Deciding dial | Next action |
|---|---|---|---|---|
| whole | skill | new skill `gate-skill-candidates` | all pass | hand admission artifacts to authoring |

Admission artifacts: the description in this skill's frontmatter; the three false-trigger utterances above; nearest neighbor `report-feedback-on-ryo-skills` (it routes feedback about existing skills; the gate rules on skills that do not exist yet).

## Example 2 — principle-vs-heuristic framework (split)

Candidate: a framework that classifies each convention as principle or heuristic and changes its treatment. It contains two parts: (A) a review-time audit procedure (run classification tests against the actual codebase, emit per-rule enforcement policies), and (B) three short generation-time rules of conduct (never present a heuristic with principle authority; enforce principles unconditionally; do not adopt a heuristic until pressure exists).

Part A — audit procedure:

| Dial | Pass/Fail | Evidence |
|---|---|---|
| Recurrence | Pass | Convention audits and "is this rule negotiable?" disputes recur across reviews and architecture decisions |
| Behavioral delta | Pass | Baseline failure: reviews flag a circular dependency and a folder-naming deviation with identical severity, and yield equally under pushback |
| Trigger fitness | Pass | False triggers: "review this PR for bugs, skip convention talk", "check GDPR compliance", "improve this function's naming"; firing moments (multi-test classification against a codebase) are complex |
| Minimal mechanism | Pass | No existing host skill covers rule-authority grading; a reference doc would not change review behavior; ad-hoc prompting loses the procedure each session |
| Context economy | Pass | Fires on convention audits and disputed reviews—moderate frequency, high value per fire (changes what gets blocked vs questioned) |

Part B — generation-time rules of conduct:

| Dial | Pass/Fail | Evidence |
|---|---|---|
| Recurrence | Pass | Every architecture proposal is an occasion |
| Behavioral delta | Pass | Baseline failure: proposals state layering heuristics with "must/never" authority |
| Trigger fitness | Fail | Under-firing direction: the rules must act ambiently during ordinary generation; models consult skills only for work they cannot easily do alone, so a standalone skill carrying three lines of conduct would never fire |
| Minimal mechanism | — | Not reached; trigger fitness already forces the route |
| Context economy | — | Not reached |

| Part | Verdict | Destination | Deciding dial | Next action |
|---|---|---|---|---|
| A: audit procedure | skill | new skill (authoring to name it) | all pass | proceed to authoring with the admission artifacts |
| B: rules of conduct | project-memory | 3 drafted lines in the target environment's always-loaded instruction file (CLAUDE.md / AGENTS.md) | trigger fitness (never fires standalone) | e.g. "State heuristics as defaults, never as musts. Enforce principles unconditionally. Adopt a heuristic only when a named pressure exists." |

The instructive point: part B is not rejected for being wrong—it is rejected as a standalone skill because the skill mechanism cannot deliver ambient conduct. Project-memory delivers exactly that: guaranteed application in every session, priced at three standing lines. Blind evaluation confirmed this routing—judges rated the always-loaded destination above a merge that would cover only the sibling's firing moments. Merge into the admitted sibling remains the fallback when the target environment has no always-loaded instruction file.
