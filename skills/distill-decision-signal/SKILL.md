---
name: distill-decision-signal
description: Remove AI slop and compress reports, research, meeting notes, status updates, reviews, explanations, and draft answers into decision-grade signal. Use when the user asks for high information density, only what matters, a concise or executive brief, decision-relevant extraction, aggressive pruning, or removal of filler, repetition, and generic AI prose. Preserve facts, uncertainty, constraints, dissent, source attribution, and user-required detail. Do not use for verbatim reproduction or creative writing where texture and voice are the point.
---

# Distill Decision Signal

## Optimize for decision loss

Compress against a target, not against a word count. Preserve the smallest faithful representation that lets the reader make the same well-informed decision, take the same action, or build the same essential mental model as the full material.

Treat brevity as a constraint. Treat decision retention, factual faithfulness, calibrated uncertainty, and fast retrieval as the objective.

## Establish the target

Identify, from the request and source material:

- the reader or decision-maker;
- the decision, action, or question the output must support;
- the time horizon and deadline;
- the binding constraints and cost of error;
- the requested format, length, and mandatory content.

Infer obvious context and proceed. Ask one focused question only when different plausible targets would materially change what survives compression. If no explicit decision exists, use the user's stated question or the minimum mental model needed to answer it as the target.

## Run the signal pass

### 1. Atomize the material

Separate the source into atomic units:

- decisions and recommendations;
- verified facts and measurements;
- evidence and source claims;
- constraints, dependencies, and thresholds;
- risks, contradictions, and exceptions;
- uncertainties and missing information;
- actions, owners, and dates;
- explanation, examples, repetition, and rhetoric.

Keep source boundaries visible. Do not blend claims from different sources into a stronger claim than either source supports.

### 2. Apply the counterfactual deletion test

For every unit, ask: **If this disappeared, could a reasonable reader change their choice, action, priority, timing, cost estimate, risk assessment, or confidence?**

Classify it:

- **Critical:** changes the decision, blocks execution, reverses a conclusion, or defines a material risk. Surface it.
- **Supporting:** establishes why a critical claim should be believed or defines its boundary. Keep the strongest version.
- **Contextual:** helps orientation but does not change the result. Merge into a label or omit.
- **Noise:** repeats, decorates, narrates, or speculates without changing the result. Delete.

Retain a minority or conflicting view when it could reverse the decision. Omit a merely interesting fact when it cannot.

### 3. Delete AI slop aggressively

Remove or replace:

- throat-clearing, scene-setting, and narration of the response;
- generic praise, vague importance claims, and promotional adjectives;
- repeated conclusions, caveats, definitions, and examples;
- exhaustive lists whose items do not change an action;
- false balance and boilerplate hedging;
- process detail that does not affect trust or reproducibility;
- abstractions such as “leverage synergies” when a concrete action is available;
- unsupported precision, causality, confidence, and recommendations;
- closing summaries that only restate the opening.

Do not delete the underlying evidence with the prose. Replace “This is a significant opportunity” with the decisive number, condition, or consequence. Replace “There are several risks to consider” with the actual top risk.

### 4. Compress without corrupting

- Merge duplicates and near-duplicates.
- Use one precise umbrella statement for a cluster only when it preserves material exceptions.
- Preserve exact numbers, dates, names, thresholds, negations, and comparison baselines.
- Preserve qualifiers that bound scope, population, time, confidence, or causality.
- Distinguish fact, source claim, inference, recommendation, and unknown when readers could confuse them.
- State “unknown” when the source cannot support a stronger conclusion.
- Prefer the strongest evidence over many weaker examples.
- Keep citations adjacent to the claims they support.

Never invent connective tissue to make a compressed narrative feel smoother. Compression may expose disagreement or missing evidence; keep that visible.

### 5. Order by consequence

Frontload the result in this order:

1. decision, answer, or current state;
2. facts that most strongly determine it;
3. material risk, uncertainty, contradiction, or exception;
4. next action, owner, and date when available;
5. optional detail only when requested or necessary for verification.

Use headings that state the content, not generic labels such as “Introduction,” “Background,” or “Conclusion.” Omit empty sections.

### 6. Run the faithfulness check

Verify each output claim against the source:

- Trace every factual statement to supplied material or a cited source.
- Mark any synthesis or inference that is not directly stated.
- Restore any omitted qualifier that could alter interpretation.
- Recheck arithmetic and units.
- Apply the reversal test: if an omitted fact could plausibly flip the recommendation, restore it.
- Preserve every user-mandated element even when it lowers compression.

For high-stakes or time-sensitive claims, verify current primary sources when the task authorizes research; otherwise flag the verification gap. Do not add external material to a source-only compression unless needed to prevent a misleading result.

## Choose the output shape

Use the smallest shape that carries the signal.

### Decision brief

Default to this for reports, research, incidents, proposals, and meetings:

```markdown
<Bottom line in 1–3 sentences>

### Decision drivers
- <fact or constraint> — <why it changes the decision>

### Material uncertainty
- <unknown, dissent, or failure mode> — <decision consequence>

### Next move
- <action> — <owner/date if known>
```

Keep only non-empty sections. Let complexity, not habit, determine bullet count.

### Dense answer

Default to this for questions and explanations:

1. Give the answer directly.
2. Give only the reasoning required to trust or apply it.
3. State the decisive boundary, exception, or uncertainty.
4. End with the next action only when one exists.

### Compression audit

Provide an audit only when requested. Report what classes of material were removed, what decision-critical material was preserved, and any compression risk. Treat word or token reduction as a diagnostic, never as the success criterion.

## Enforce dense style

- Match the user's language and level of technicality.
- Make each sentence carry a claim, evidence, implication, constraint, or action.
- Prefer concrete nouns, strong verbs, and informative headings.
- Use bullets for parallel facts, not to fragment a coherent argument.
- Put the differentiator before shared background.
- Avoid meta-openers such as “Here is a concise summary.”
- Avoid “overall,” “in conclusion,” “it is important to note,” and similar filler unless they add meaning.
- Do not impose artificial symmetry, fixed list lengths, or a tidy narrative on uneven evidence.
- Stop deleting when another deletion would increase decision loss.

## Definition of done

Finish only when:

- the first screen exposes the answer or decision;
- every retained sentence passes the counterfactual deletion test;
- no unsupported claim, false precision, or hidden contradiction remains;
- all decision-flipping constraints and qualifiers survive;
- the reader can identify the next move or the reason no move is justified;
- further shortening would remove decision value rather than prose waste.

Read [references/research-basis.md](references/research-basis.md) only when adapting this method, explaining its rationale, or resolving a difficult tradeoff between brevity and fidelity.
