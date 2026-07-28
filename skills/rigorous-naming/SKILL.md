---
name: rigorous-naming
description: Apply rigorous naming to non-trivial identifiers and domain vocabulary during implementation, refactoring, review, and verification. Use before work adds, renames, repurposes, translates, abbreviates, broadens, or narrows names in modules, types, functions, fields, APIs, schemas, configuration or CLI keys, events, telemetry, errors, tests, or documentation, even when naming is incidental to a larger task. Use audit mode only for explicit report-only requests. Skip generated or vendored code, mechanically prescribed names, established terms of art, and conventional tiny-scope locals.
---

# Rigorous Naming

## Default Behavior

Treat names as design decisions, domain-model decisions, and contracts with readers and consumers. Apply this workflow before writing the first non-trivial proposed name into a file.

Default to **embedded mode** during implementation. Make the naming decision inside the authorized task and continue the implementation. Do not turn ordinary implementation into an advisory report or ask for approval for a reversible local/private name.

## Select The Mode

| Request | Mode | Behavior |
|---|---|---|
| A feature, fix, refactor, schema change, or documentation change introduces or changes names | **Embedded** | Run the workflow, implement the chosen vocabulary, and verify propagation |
| The user asks to improve one or more specific existing names | **Improve** | Diagnose the current meaning, compare replacements, and implement changes within the authorized scope |
| The user explicitly asks for a naming audit, review, candidate list, or report only | **Audit** | Report findings without editing |

When the request is ambiguous, use embedded mode if it authorizes a change; use audit mode only when it clearly asks for analysis without mutation.

## Apply The Scope Gate

Run the full workflow for a non-trivial name that can carry meaning beyond one obvious expression or tiny local scope. Include domain terms and names exposed through code, tests, APIs, schemas, persistence, configuration, CLI surfaces, events, telemetry, errors, and documentation.

Do not require candidate comparison for:

- generated or vendored code;
- names prescribed by a language, framework, protocol, or external standard;
- established terms of art used with their established meaning;
- conventional locals whose meaning is completely constrained by a tiny scope, such as `i` in a short loop;
- a mechanical correction to the already-established canonical spelling when no semantic choice exists.

Never use an exemption to preserve a misleading name.

## Run The Decision Procedure

### 1. Inventory Existing Language

Search before choosing. Search for the proposed term, prior term, inflections, abbreviations, synonyms, antonyms, and adjacent concepts. Inspect representative declarations and use sites across every affected surface.

Distinguish absence from discovery failure. Do not create a new term until the search shows that no existing canonical term expresses the same concept precisely.

### 2. Define The Concept

Write one working sentence in this form:

> In `<bounded context>`, `<term>` means `<definition>`; it includes `<included cases>` and excludes `<excluded cases>`.

If the sentence cannot be completed, investigate the domain and responsibility before naming. Do not hide uncertainty behind a polished identifier.

### 3. Classify The Surface

Classify the name before changing it:

- **Local/private:** reversible implementation detail.
- **Shared vocabulary:** repository-wide or bounded-context language used by multiple components or documents.
- **Public/persisted:** API, schema, wire format, event, CLI, configuration, telemetry, serialized data, database, or another externally consumed contract.

Treat public/persisted renames as compatibility and migration work, even when the surface is labeled experimental.

### 4. Choose Concepts Before Words

List the concepts the name must express. Select one canonical word for each concept, then compose the identifier according to the host language and surrounding context.

Maintain one canonical term per concept and one meaning per term inside a bounded context. Do not add a synonym for novelty, brevity, translation convenience, or personal preference.

### 5. Compare Serious Candidates At Use Sites

For a genuine non-trivial choice, compare at least two serious candidates. Place each candidate at:

- its declaration;
- representative call or access sites;
- a test name;
- an error or diagnostic when applicable;
- a documentation sentence when applicable.

Reject a candidate that is truthful only at the declaration but misleading where readers use it. Prefer precision and honesty before brevity. Let the receiver, module, and type supply context instead of repeating it.

Read [references/calibration.md](references/calibration.md) when candidates remain close, when auditing, or when evaluating this skill.

### 6. Treat Naming Difficulty As Design Evidence

Investigate the design before abbreviating when:

- every honest name is long or joined by multiple actions;
- the definition changes between call sites;
- a broad word such as `Manager`, `Util`, `Data`, `Info`, `Item`, `Process`, or `Handle` seems necessary;
- several parameters or fields repeatedly travel together;
- the name describes timing or mechanics but not purpose;
- one established term is being stretched across distinct concepts.

These words are signals, not blanket bans. Keep one when it is the precise established term in that context.

Read [references/design-signals.md](references/design-signals.md) when a signal appears or the user requests design-level refactoring.

### 7. Decide, Implement, And Propagate

Choose the candidate that best matches the definition and reads naturally at use sites. Then propagate the canonical term through every affected code, test, API, schema, persistence, configuration, CLI, event, telemetry, error, and documentation surface.

For local/private decisions, proceed without waiting. For shared vocabulary, update an existing glossary or domain document when the repository has one. Do not create a glossary solely to record one obvious term.

For public/persisted changes, identify consumers and establish the safe path: preserve the current name, add a compatible alias, deprecate it, version the contract, or migrate consumers and stored data. Ask before proceeding only when the required compatibility strategy is not already authorized or discoverable.

### 8. Verify The Vocabulary

Search again for:

- the previous term and spelling;
- rejected synonyms and abbreviations;
- conflicting uses of the selected term;
- callers, consumers, fixtures, snapshots, generated artifacts, and migration code;
- documentation or telemetry that still teaches the old vocabulary.

Run the relevant tests and compatibility checks. A passing test suite does not by itself prove that the vocabulary is coherent.

## Handle Audit Mode

Audit only the scope the user names. Report each consequential issue with the current term, observed meaning, evidence from use sites, conceptual conflict, affected surface, and recommended next decision. Include safe counterexamples so the report does not become a blanket style critique.

Do not edit in audit mode. If the user later asks to apply a finding, switch to improve mode for that scope without repeating the full audit.

## Escalate Only At Contract Boundaries

Ask the user only when:

- the domain evidence supports multiple materially different definitions;
- the change would merge or split established concepts;
- a public/persisted rename lacks an authorized compatibility strategy;
- resolving the name requires an API, schema, permission-boundary, or other structural expansion outside the task.

Present the competing definitions, strongest candidates, consequential difference, and migration impact. Do not ask the user to choose between names without this evidence.

## Definition Of Done

Do not finish a task that introduces or changes a non-trivial term until:

- the selected term has a one-sentence definition with context and exclusions;
- an important alternative has been compared and rejected for a concrete reason;
- representative declarations and use sites have been inspected;
- the selected term has been propagated across affected surfaces;
- stale and competing terms have been searched again;
- compatibility impact has been handled or explicitly reported.

In the final response, report the selected term and definition, rejected alternative and reason, searched or updated surfaces, and compatibility impact. Omit this bookkeeping for exempt tiny-scope or mechanically prescribed names.

## License And Attribution

This skill is an adaptation of `evolutionary-naming` by kawasima. See [ATTRIBUTION.md](ATTRIBUTION.md) for the source, license, upstream notices, and a description of the changes. This skill directory is licensed under [CC BY 4.0](LICENSE).
