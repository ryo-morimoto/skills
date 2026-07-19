# Research Basis, Inference, and Limits

Use sources to bound a recommendation, not to claim a universal productivity effect. “Skill synthesis” below is an inference from the cited evidence, not a directly tested combined method.

## Evidence map

| Evidence | Reported result | Supports | Does not establish |
|---|---|---|---|
| [NaPiRE: 228 companies, 10 countries](https://arxiv.org/abs/1611.10288) | Incomplete/hidden requirements, communication flaws, weak customer access, unclear quality, infeasibility, and volatility recur; causes/effects vary by context. | Diagnose the kind and context of a requirement problem before applying a practice. | One globally optimal RE process or causal productivity gain. |
| [Requirements-quality mapping: 105 studies](https://link.springer.com/article/10.1007/s00766-021-00367-z) | Ambiguity, completeness, and consistency dominate research; only about 9% of studies applied the approach industrially. | Treat textual quality checks as partial and prescriptions cautiously. | That linting or templates resolve semantic/domain uncertainty. |
| [Quality User Story: 13 criteria; >1,000 stories, 18 organizations](https://link.springer.com/article/10.1007/s00766-016-0250-x) | Distinguishes automatable clerical defects from semantic understanding. | Use tooling for detectable form defects; route meaning to human/domain evidence. | Automated validation of business correctness or value. |
| [Twin Peaks](https://doi.org/10.1109/2.910904) | Requirements and architecture should elaborate concurrently; architecture exposes feasibility, constraints, and alternatives. | Produce provisional requirements and design together. | That any particular architecture method or artifact set is mandatory. |
| [RE4SA real-world cases](https://www.sciencedirect.com/science/article/pii/S0950584921000239) | Alignment/granularity analysis exposes problematic requirement–architecture relationships; more validation is needed. | Trace design decisions to requirement drivers and mismatched granularity. | Broad causal superiority over other approaches. |
| [SEI Quality Attribute Workshop](https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/) | Stakeholders refine/prioritize scenarios using stimulus, environment, response, and trade-offs. | Replace quality adjectives with testable operating scenarios. | Universal thresholds or that workshops are always the cheapest format. |
| [Quality requirements: 4 companies, 36 interviews](https://link.springer.com/article/10.1007/s10664-020-09903-x) | Proactive, reactive, and interactive strategies coexist; practices and challenges depend on context. | Select evidence/coordination by local risk and lifecycle instead of one ceremony. | One fixed quality-requirements process. |
| [Prototyping mapping + 12-company study](https://link.springer.com/article/10.1007/s10664-023-10331-w) | Prototypes concretize requirements; production-code prototypes can imply false readiness and carry security/robustness/scalability risk. | Bind prototypes to hypotheses/decisions and mark fidelity/readiness limits. | That prototypes are production evidence or always reduce rework. |
| [Continuous clarification in a software ecosystem](https://link.springer.com/article/10.1007/s00766-016-0259-1) | Relevant emergent contributors can change requirement discussion; late participation can create rework. | Involve owners of consequential dependencies before boundary decisions harden. | Invite every possible stakeholder or create permanent broad forums. |
| [Longitudinal 10-team coordination case](https://link.springer.com/article/10.1007/s10664-022-10230-6) | Removing coordination mechanisms wholesale worsened coordination; dependency-linked mechanisms later re-emerged. | Coordinate actual dependencies and preserve necessary mechanisms. | Copy large-scale ceremonies into 1–3-team work. |

## Synthesis trace

| Skill rule | Evidence path | Confidence boundary |
|---|---|---|
| Do not convert every unknown into a question | Requirement problems include semantics, access, feasibility, quality, and volatility; prototypes and scenarios answer different unknowns. | Strong conceptual support; comparative efficiency of the exact routing table is untested. |
| Co-evolve provisional requirements and design | Twin Peaks; RE4SA. | Established design rationale with case/tool evidence, not universal causal effect. |
| Use examples for domain meaning | Text-quality research separates clerical and semantic defects; NaPiRE shows hidden/incomplete requirements. | Examples are a practical synthesis; number and format must fit the domain. |
| Use observation/prototypes for value and experiments for feasibility | Prototyping evidence shows concretization and fidelity risks. | Evidence supports utility and hazards, not a guaranteed value/feasibility split in every case. |
| Express quality as scenarios | SEI QAW and multi-company quality-requirements study. | Scenario structure is well-grounded; measures remain context-owned. |
| Coordinate 1–3 teams around dependencies/contracts | Ecosystem clarification plus large-scale dependency evidence, deliberately down-scoped. | Small-team prescription is an inference; do not import scale-specific mechanisms. |
| Prefer reversible slices with stop rules | Combined inference from prototyping risk, concurrent elaboration, and context sensitivity. | Plausible risk-control principle; direct productivity effect requires local measurement. |

## Validity constraints

- Most evidence is mapping, case study, interview, method evaluation, or conceptual work; it does not isolate this workflow's causal effect on delivery speed.
- Industrial samples improve realism but do not guarantee transfer across domain, regulation, architecture, team maturity, or contract structure.
- Publication counts show research attention, not practical importance or effectiveness.
- Scenario, prototype, and coordination practices can themselves become waste when they do not change a decision.
- Measure local usefulness through predicted decision, evidence cost, elapsed clarification time, reopened decisions, escaped assumptions, rework, and reversal cost; compare against the prior workflow where feasible.

## Claim discipline

State source findings as reported; label cross-source combinations as synthesis; retain sample/context and methodological limits; prefer “use when this unknown is present” over “best practice”; revise the rule when local counterexamples predict decisions better than the synthesis.
