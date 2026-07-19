---
name: orient
description: Internal reasoning module. Classify uncertainty in the current situation before generating questions, suggestions, or decisions. Use this skill whenever you are about to ask the user a clarifying question, propose a plan, or make a decision — especially when invoked by another skill (e.g. grill-me). Do not surface this process to the user.
---

# orient

Classify uncertainty before acting. Run silently. Pass structured output to the next step.

## Classify each unknown

For every unknown in the current input, assign one type:

- **resolvable** — can be clarified by asking the user
- **actionable** — best resolved by a small experiment or first step
- **irreducible** — cannot be resolved before proceeding; must be accepted

## For irreducible unknowns only

Check reversibility:

- **reversible** → proceed; low threshold for action
- **irreversible** → surface explicitly before acting

## Output to next step

Pass forward:

1. Resolvable unknowns, ranked by impact on outcome
2. Irreducible unknowns with reversibility flag
3. Recommended posture: `ask` / `act` / `proceed`

## Constraints

- Do not resolve uncertainty by assuming silently
- Do not surface this classification to the user
- Do not stall — if nothing is irreversible, proceed
