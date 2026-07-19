# Research basis

This reference records the design basis for the workflow. Treat the mappings below as design inferences unless a source directly prescribes the exact practice.

## Skill architecture

- [OpenAI Codex manual: Build skills](https://developers.openai.com/codex/codex-manual.md#build-skills) defines a skill as instructions plus optional scripts and references. It describes progressive disclosure: metadata is visible first and the full `SKILL.md` loads only after selection. It also says implicit activation depends on a concise, clearly scoped, frontloaded description. Design consequence: keep the trigger precise, keep the core workflow in `SKILL.md`, and move rationale here.
- The official `skill-creator` guidance adds three useful constraints: assume the model already knows general material, spend context only on non-obvious procedure, match prescriptiveness to task fragility, and validate the installed skill. Design consequence: use a compact instruction-only workflow with strict fidelity guardrails and no deterministic script.

## Compression objective

- Tishby, Pereira, and Bialek, [“The information bottleneck method”](https://arxiv.org/abs/physics/0004057), formalize compression as finding a short code for one signal that preserves maximal information about a relevant target. Design inference: define the target as the reader's decision, action, or essential mental model; remove information that does not help predict or determine that target.
- Howard, [“Information Value Theory”](https://ieeexplore.ieee.org/document/4082064/), joins uncertainty with the economic consequences of decisions and assigns value to reducing uncertainty. Design inference: judge a content unit by whether its presence can change choice, action, risk, or confidence—the counterfactual deletion test—rather than by whether it is generally informative.

## Cognitive and retrieval constraints

- Sweller, [“Cognitive Load During Problem Solving: Effects on Learning”](https://doi.org/10.1016/0364-0213(88)90023-7), reports that demanding means-ends processing consumes limited cognitive capacity that is then unavailable for schema acquisition. Design inference: delete extraneous processing demands and organize the surviving relationships so the reader can allocate attention to the decision.
- Liu et al., [“Lost in the Middle: How Language Models Use Long Contexts”](https://aclanthology.org/2024.tacl-1.9/), find that model performance changes with the position of relevant information and often degrades when it appears in the middle of a long context. Design consequence: frontload the result and strongest drivers; do not assume a long context guarantees robust retrieval.

## Faithful summarization

- Maynez et al., [“On Faithfulness and Factuality in Abstractive Summarization”](https://aclanthology.org/2020.acl-main.173/), find substantial hallucinated content in model-generated abstractive summaries and report that entailment-oriented measures correlate with faithfulness better than standard overlap metrics. Design consequence: require claim-level traceability, retain source boundaries and qualifiers, and never optimize compression ratio alone.

## Content design

- [GOV.UK content design guidance](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/understand-content-design/) starts with the user's need and explicitly permits reducing, splitting, changing, or removing content to avoid duplication or conflict. Design consequence: define the reader's job before editing and remove material that does not serve it.
- The UK Office for National Statistics, [“Structuring content”](https://service-manual.ons.gov.uk/content/writing-for-users/structuring-content), recommends frontloading, an inverted pyramid, descriptive headings, and checking each content unit against prioritized user needs. It distinguishes must-have information, understanding-supporting information, and helpful but nonessential information. Design consequence: order by consequence and use the Critical / Supporting / Contextual / Noise classification.

## Limits

- Information-theoretic compression does not by itself determine semantic or practical value; the decision target supplies that relevance criterion.
- Cognitive-load research is primarily about learning and problem solving, not a universal proof that shorter text is always better.
- Frontloading and aggressive pruning can hide nuance if used mechanically. Preserve contradictions, decision-flipping exceptions, and uncertainty even when they reduce apparent density.
- A high compression ratio can coexist with a bad summary. Evaluate retained decision value and faithfulness first.
