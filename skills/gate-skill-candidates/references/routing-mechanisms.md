# Routing mechanisms

Read this file after assigning any non-skill verdict, before writing the routing output. Each destination has a cost profile—standing cost / firing precision / maintenance—and a required output shape.

## Merge into an existing skill

Profile: no new standing cost / inherits the host's firing precision / host grows and must stay within its line budget.

- Locate the receiving section in the host skill and name it in the Destination column.
- Quote the host's current description and confirm it still covers the merged capability without rewriting; if absorption would force the description to widen, the merge is suspect—widening a description degrades the host's own trigger precision.
- Check the host's body stays well under its line budget after absorption; if not, propose the content as a new reference file inside the host instead of body text.
- The merged content fires only when the host fires. If the candidate's moments of use are not a subset of the host's, the merge silently drops the difference—say so explicitly.

## Project-memory

Profile: standing cost of a few lines in every session / firing precision perfect—ambient, no trigger to miss / low maintenance.

- Use for always-on conduct and short constant rules: content that must apply during ordinary work, where a trigger-dependent skill would never fire (the never-fires early exit lands here).
- Draft the actual lines—three or fewer, imperative—and name the destination file: the target environment's always-loaded instruction file (CLAUDE.md, AGENTS.md, or equivalent).
- The lines are paid in every session; that is the point, and also the budget. If the content cannot compress to a few lines, it is not project-memory material—reconsider merge or split.
- When the target environment has no always-loaded instruction file, say so and fall back to merge into the skill that fires nearest to the relevant moments, naming the coverage that is lost.

## Reference document only

Profile: zero standing cost, zero trigger cost / never fires on its own—it is found, not triggered / low maintenance.

- Use for knowledge worth keeping that changes no behavior: background, rationale, research notes, worked analyses.
- Name the concrete file and where it lives (a `docs/` path, or a `references/` file inside a related skill).
- Do not dress a reference document as a skill to make it "discoverable"; a skill that only conveys knowledge fails behavioral delta.

## No build

Profile: zero cost / not applicable / zero maintenance.

- Correct when a one-off prompt suffices, when recurrence is anticipatory, or when no mechanism would change behavior at all.
- Say so without apology and without hedging into "maybe later": name the condition that would reopen the gate (for example, "the third real occurrence" or "an observed baseline failure").
- No-build prices mechanism fit, not idea quality. State what the idea is worth outside the skill mechanism when that is genuinely useful.

## Split

- Gate each part independently; one verdict per part (one scorecard and routing row per part in full format).
- Parts may land anywhere, including different destinations for each part. Treat a split that yields two new skills with suspicion under context economy—two admissions must each clear the tax on their own.
- A part that fails trigger fitness in the under-firing direction routes to project-memory first—ambient application is what it needs. Merge into an admitted sibling is the fallback when no always-loaded file exists, and it covers only the moments the sibling fires; name that loss.
