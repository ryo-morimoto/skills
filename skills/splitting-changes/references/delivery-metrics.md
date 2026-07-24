# Delivery-metric calibration

Use this guide only for team-level policy or after enough completed changes exist to estimate local behavior.

## Measure

Collect, with consistent definitions:

- changed lines and files per PR or landed unit;
- review wait time and active review time;
- rework after review;
- escaped defects or change failure rate;
- deployment lead time;
- restoration time;
- fixed transaction costs such as CI and deployment duration;
- change complexity or risk class where possible.

Separate generated code, formatting, vendored code, and mechanical renames from semantic churn.

## Calibrate

1. Plot local size distributions against review latency, rework, and failures.
2. Stratify or adjust for complexity, change type, ownership, and subsystem.
3. Set a warning line where local outcomes begin to degrade or reviewers report context overload.
4. Keep the threshold advisory unless the team has strong local evidence for a gate.
5. Re-evaluate periodically after tooling, architecture, or team composition changes.

The commonly repeated 200–400 line range comes from a non-peer-reviewed vendor study. It can seed a warning, not establish a universal limit.

## Detect under- and over-splitting

Possible under-splitting signals:

- review latency and false-positive comments rise with batch size;
- units repeatedly contain unrelated rework;
- rollback scope is broad;
- reviewers cannot state the change intent.

Possible over-splitting signals:

- coordination and CI fixed costs dominate;
- many units have no independent verification or value;
- stacked dependencies create more wait time than risk reduction;
- failure rate or lead time worsens while frequency alone improves.

Balance transaction cost against delay and risk. Do not maximize deployment frequency by itself.

## Evidence boundary

DORA-style delivery metrics are useful operational signals, but their widely cited relationships are primarily observational and survey-based. Treat them as correlated indicators and local feedback, not proof that increasing one metric causes the others to improve.
