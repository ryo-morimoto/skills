# Research Basis, Inference, and Limits

Use sources to bound the workflow's rules, not to claim a proven productivity effect. "Skill synthesis" below is an inference from the cited evidence; the combined workflow has not itself been empirically tested.

## Evidence map

| Evidence | Reported result | Supports | Does not establish |
|---|---|---|---|
| [Snowden & Boone, A Leader's Framework for Decision Making, HBR 2007](https://hbr.org/2007/11/a-leaders-framework-for-decision-making) | Clear, complicated, complex, and chaotic contexts call for different responses: categorize-and-respond, expert analysis, or probing experiments. | Routing by dominant uncertainty: `auto` for clear work, human analysis/decision for complicated tradeoffs, evidence slices (spikes, discarded PRs) as probes for complex work. | Crisp objective boundaries between contexts; classification remains judgment, which is why the gate demands cited evidence per condition. |
| [Fairbanks, Just Enough Software Architecture, 2010](https://georgefairbanks.com/book/) | Risk-driven model: do architecture work commensurate with failure risk, then stop. | Skipping design ceremony on gate-passing issues; spending design only where conditions 2, 3, or 5 fail. | Universal thresholds for "enough" design; the five conditions are this skill's operationalization, not Fairbanks's. |
| [Nuseibeh, Weaving Together Requirements and Architectures (Twin Peaks), 2001](https://doi.org/10.1109/2.910904) | Requirements and architecture should elaborate concurrently; architecture exposes feasibility and alternatives. | The feedback edge from verification back to design/triage: implementation evidence legitimately reopens requirements and design. | That any particular artifact set is mandatory in the design phase. |
| [Boehm, Verifying and Validating Software Requirements and Design Specifications, IEEE Software 1984](https://doi.org/10.1109/MS.1984.233702) | Verification ("building the product right") and validation ("building the right product") answer different questions. | Two separate downstream gates: merge on verification, close only on acceptance; acceptance rejection re-enters triage as a requirements problem. | That the split removes the need for either gate, or specific acceptance-test techniques. |
| [DORA capability: Working in small batches](https://dora.dev/capabilities/working-in-small-batches/) / [Trunk-based development](https://dora.dev/capabilities/trunk-based-development/); Forsgren, Humble & Kim, *Accelerate*, 2018 | Survey analysis associates small batches, frequent trunk merges, and short-lived branches with higher delivery performance and stability. | Decomposing into independently mergeable slices; one-issue-one-PR; discarding rather than growing a drifting PR. | Causality for any single team; findings are correlational survey research. |
| [Bacchelli & Bird, Expectations, Outcomes, and Challenges of Modern Code Review, ICSE 2013](https://sback.it/publications/icse2013.pdf) | Change understanding is the limiting factor of modern review; outcomes are knowledge transfer and defect finding, constrained by context. | Requiring the diff to trace to a recorded requirement/decision so reviewers get the context understanding needs. | Numeric size limits; the two-repair-round bound is this skill's control, not a finding. |
| [SmartBear/Cisco peer review study](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/) | Defect-detection effectiveness drops as review size grows beyond roughly 200–400 LOC. | Keeping slices small enough to review as one unit. | A precise threshold; industry study, not peer-reviewed, numbers are context-bound. |
| [Wake, INVEST in Good Stories, 2003](https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/) | Good backlog items are Independent, Negotiable, Valuable, Estimable, Small, Testable. | Sub-issue quality bar in the split route: own observable behavior, own done criteria, independently verifiable. | Empirical validation; INVEST is a practitioner heuristic. |
| [Nygard, Documenting Architecture Decisions, 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | Lightweight records of context, decision, and consequences keep decisions revisitable. | The decision-record comment (context, options, accepted loss, revisit trigger) as the interface between design and implementation. | That ADRs alone improve outcomes; the practice is widely adopted but thinly measured. |
| Boehm, *Software Engineering Economics*, 1981 — with later critiques of the "cost-of-change curve" evidence base | Reported defect-repair cost escalates by phase; the underlying data has been credibly challenged as thin for modern iterative development. | Directionally: feed implementation failures upstream to the invalidated decision instead of patching downstream symptoms. | Any exponential cost multiplier; treat "fix upstream" as a loss-control heuristic, not a quantified law. |
| Brooks, *The Mythical Man-Month* ("plan to throw one away") | A first implementation often functions as discovery, not product. | Treating a discarded PR as purchased evidence — the feedback record captures what the attempt taught. | That discarding is always cheaper than repairing; hence the bounded-repair path for execution-level defects. |

## Synthesis trace

| Workflow rule | Evidence path | Confidence boundary |
|---|---|---|
| Five-condition upstream gate | Cynefin (route by context) + Fairbanks (risk-proportional design) + Boehm V&V (verifiability as a first-class condition) | The specific five conditions and the safety ceiling are this skill's synthesis; measure locally which conditions actually predict failed cycles. |
| Split into re-triaged vertical slices, one level deep | INVEST + DORA small batches + review-size evidence | Slice quality criteria are heuristic; the one-level depth limit is a convergence control, not a finding. |
| Merge on verification, close on acceptance | Boehm V&V; acceptance rejection routed to triage follows Twin Peaks feedback | Gate order is well-grounded conceptually; acceptance practice remains context-owned. |
| Discard PR on decision-level failure, two-round repair bound | Brooks + cost-of-change direction + sunk-cost avoidance; small-batch evidence makes discard cheap | The number two is a chosen budget. Tune it; the non-negotiable part is that unbounded repair is decision-level failure denial. |
| State on the issue as labels + marked comments | ADR practice extended from architecture decisions to workflow state | Convention, not research; its value is resumability and auditability, both locally observable. |

## Validity constraints

- No cited study tested this workflow end to end; evidence supports individual rules at different strengths, from survey correlation (DORA) to practitioner heuristic (INVEST, ADR).
- Cynefin classification and gate verdicts are judgment calls; two competent judges can route the same issue differently. The triage record exists so disagreement is visible and correctable, not so it disappears.
- The DORA association between small batches and performance comes from cross-company surveys; transfer to a single team, domain, or regulated context is not guaranteed.
- Autonomous-implementation safety depends on test-suite quality, which no gate condition can fully observe; a green verification on a weak suite is a false pass.
- Measure the workflow locally: cycle time per route, discarded-PR rate and what each discard taught, acceptance rejections traced to which gate condition missed them, and repair rounds used. Rules that never fire or always fire are miscalibrated.

## Claim discipline

State source findings as reported; label cross-source combinations as synthesis; keep sample and context limits attached; prefer "route this way when this condition fails" over "best practice"; revise the gate when local cycle data predicts outcomes better than the synthesis does.
