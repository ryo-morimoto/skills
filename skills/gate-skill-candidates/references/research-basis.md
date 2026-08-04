# Research basis

This reference records the sources behind the five dials and the two early-exit rules. Read it only when the user challenges the gate's strictness or asks to tune a dial. Treat the mappings below as design inferences unless a source directly prescribes the exact practice.

## Cost model (context economy dial)

- Anthropic, [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), opens with "The context window is a public good" and specifies the loading model: at startup only the name and description of every skill are pre-loaded; the SKILL.md body loads when the skill triggers; bundled files load on demand. Design consequence: the standing tax of an admitted skill is its metadata in every session, and the body cost is paid on every fire—both sides of the context-economy dial.
- The same guide states the description is how Claude selects "the right Skill from potentially 100+ available Skills". Design inference: every admission makes that selection marginally harder for all existing skills—the selection externality the context-economy dial charges against the candidate.

## Behavioral delta dial

- The same guide's "Default assumption: Claude is already very smart. Only add context Claude doesn't already have"—with the challenge questions "Does Claude really need this explanation?" and "Does this paragraph justify its token cost?". Design consequence: a candidate whose content the model already applies when asked has no behavioral delta and fails the dial.
- The guide's evaluation-driven development section instructs: "Create evaluations BEFORE writing extensive documentation. This ensures your Skill solves real problems rather than documenting imagined ones", starting from "Run Claude on representative tasks without a Skill. Document specific failures or missing context" and "Establish baseline". Design consequence: the dial's required evidence is a named, observed baseline failure, not a hypothesized one.

## Recurrence dial

- The guide's recommended creation flow starts from completing a real task without a skill and noticing "what information you repeatedly provide", and warns against "anticipating requirements that may never materialize". Design consequence: the recurrence dial demands occasions that actually happened or are concretely foreseeable, and rejects anticipatory candidates.

## Trigger fitness dial

- The guide requires descriptions to be third person, specific, keyword-bearing, and to state both what the skill does and when to use it; vague descriptions ("Helps with documents") are listed as anti-patterns. Design consequence: the over-firing direction of the dial—three concrete false-trigger utterances distinct from every existing description—operationalizes "specific enough to select against neighbors".
- The official `skill-creator` skill (bundled with Claude Code) reports two triggering facts: Claude currently tends to under-trigger skills, so descriptions should be somewhat "pushy"; and "Claude only consults skills for tasks it can't easily handle on its own — simple, one-step queries … may not trigger a skill even if the description matches perfectly." Design consequence: the under-firing direction of the dial—content that must act ambiently, or whose moments of use are one-step wishes, cannot be delivered through the skill mechanism at all. This is the "skill that would never fire" early exit.

## Shape of admission artifacts

- The guide's structural rules—body under 500 lines, references one level deep with explicit read conditions, a table of contents for reference files over 100 lines, consistent naming within a collection—define what an admitted candidate must eventually satisfy. Design consequence: the gate's draft-description artifact follows the third-person what+when+not shape, and authoring inherits the structural budget.

## Blind evaluation of this gate (iteration 1, 2026-08)

Six behavioral evals were run with and without the skill, then re-judged two ways: format-blind outcome assertions (no gate vocabulary), and blind A/B comparison by judges who did not know which response used the skill.

- Reported findings: on outcome-only assertions the gap nearly closed (21/21 with skill vs 19/21 without—the two surviving differences were "assessed before building" and "recorded that review was skipped"). Blind judges preferred the baseline on all four advisory-form prompts, consistently calling the scorecard, routing table, and inventory narration "noise" and "jargon-heavy scaffolding"; they preferred the gate on both imperative build prompts. On the split case, judges rated routing always-on conduct to CLAUDE.md above merging it into a sibling skill with known coverage loss.
- Design consequences: the compact-verdict reply shape for advisory questions and early exits; the build-moment focus of the mode table; project-memory restored as a routing destination. The model already judges skill-worthiness well when asked—the gate's behavioral delta lives where nobody asks: at build moments, and in the audit trail.

## Limits

- Triggering behavior is model- and version-dependent; the under-trigger finding and the one-step-query finding are reported observations of current models, not permanent laws. Re-check them when tuning the trigger-fitness dial.
- The cost model describes Anthropic's skill runtime; other runtimes that load skills differently shift the context-economy arithmetic.
- The dials price mechanism fit, not idea quality: a no-build verdict says the skill mechanism is the wrong delivery vehicle, not that the idea is worthless.
- The blind evaluation ran one execution per condition and one judge per prompt; treat its direction (bloat over leniency, value at build moments) as established and its magnitudes as rough.
