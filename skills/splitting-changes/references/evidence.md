# Evidence guide

Use this guide to explain why the gates have different strengths. Do not overstate causality.

## Evidence ranks

- **A — controlled evidence**: supports a causal interpretation within the experiment’s limits.
- **B — observational evidence**: shows association and may contain selection effects or confounding.
- **C — non-peer-reviewed industry evidence**: useful as a starting reference, not a universal rule.
- **Normative**: engineering reasoning or established practice without a direct causal estimate.

## What the evidence supports

### Change decomposition

di Biase et al. (PeerJ Computer Science, 2019; DOI `10.7717/peerj-cs.193`) found a statistically significant reduction in false-positive review comments for decomposed changes in a small controlled experiment. It did not find significant improvements in detected defects, review time, or change understanding. Describe the likely first-order benefit as reduced review noise, not guaranteed defect discovery.

### Cohesion and locality

Controlled and empirical work on review performance, delocalization, and tangled commits supports keeping related reasoning local and avoiding multiple concerns in one change. This motivates the single-intent and dependency-cluster checks. It does not establish a universal textual rule for detecting intent.

Relevant sources:

- Baum, Schneider, and Bacchelli, EMSE 2019, DOI `10.1007/s10664-018-9676-8`.
- Dunsmore, Roper, and Wood, IEEE Software 2003, DOI `10.1109/MS.2003.1207450`.
- Herzig, Just, and Zeller, EMSE 2016, DOI `10.1007/s10664-015-9376-6`.
- Herbold et al., EMSE 2022, DOI `10.1007/s10664-021-10083-5`.

### Automated untangling

Dependency graphs, lexical flows, and learned models can propose clusters, but published methods use differing datasets and metrics and retain meaningful absolute error. Keep automated results reviewable and require confirmation before changing live history or publishing a series.

Relevant sources include ClusterChanges (ICSE 2015), Flexeme (FSE 2020; DOI `10.1145/3368089.3409693`), SmartCommit (FSE 2021; DOI `10.1145/3468264.3468551`), and UTango (FSE 2022; DOI `10.1145/3540250.3549171`).

### Requirement selection

The Next Release Problem formalizes selecting requirements under value, cost, and precedence constraints. It supports making those fields explicit and selecting dependency-closed sets. It does not prove that a particular story-splitting pattern finds the best semantic boundaries.

Relevant sources include Baker et al. (ICSM 2006), Veerapen et al. (IST 2015), and Li et al. (IEEE TSE 2016).

### Size thresholds

Large changes are often associated with worse review outcomes, but complexity and other factors confound observational results. The often-cited 200–400 line range traces to a non-peer-reviewed SmartBear/Cisco study. Use a local warning threshold and recalibrate it; never claim a universal causal cutoff.

### Delivery performance

DORA and Accelerate provide useful system-level measures, but their main evidence is observational and survey-based. Do not claim that increasing deployment frequency alone causes better stability or throughput.

## Communication rules

- Label causal, correlational, vendor, and normative claims.
- State material sample or external-validity limits when using a study to justify a gate.
- Prefer “suggests,” “is associated with,” or “motivates” for non-causal evidence.
- Keep unknowns visible: optimal size cutoffs, fully automatic untangling accuracy, and the causal effect of requirement slicing remain unresolved.
