---
name: rigorous-naming
description: Apply rigorous naming to non-trivial identifiers and domain vocabulary during implementation, refactoring, improve, audit, and verification. Use before work adds, renames, repurposes, translates, abbreviates, broadens, or narrows names in modules, types, functions, fields, APIs, schemas, configuration or CLI keys, events, telemetry, errors, tests, or documentation—even when naming is incidental. Use verify mode when the user asks only to check adopted or proposed terms. Use audit mode only for improvement inventories without mutation. Skip generated or vendored code, mechanically prescribed names, established terms of art, and conventional tiny-scope locals.
---

# Rigorous Naming

## Default Behavior

Treat names as design decisions, domain-model decisions, and contracts with readers and consumers. Apply this workflow before writing the first non-trivial proposed name into a file.

Default to **embedded mode** during implementation. Make the naming decision inside the authorized task and continue the implementation. Do not turn ordinary implementation into an advisory report or ask for approval for a reversible local/private name.

When the [scope gate](#apply-the-scope-gate) requires the full workflow for any term, the task is incomplete until **Naming decisions** is emitted in the final response. That display threshold is identical to the scope gate—not a separate, softer rule.

## Select The Mode

| Request | Mode | Behavior |
|---|---|---|
| A feature, fix, refactor, schema change, or documentation change introduces or changes names | **Embedded** | Run the workflow, implement the chosen vocabulary, verify propagation, emit Naming decisions |
| The user asks to improve one or more specific existing names | **Improve** | Diagnose the current meaning, compare replacements, implement within scope, emit Naming decisions |
| The user asks only to check whether adopted or proposed terms are sound | **Verify** | Rebuild definitions and use-site evidence for the named scope; emit Naming decisions with Status; do not edit unless asked |
| The user asks for a naming audit, opportunity list, candidate inventory, or smell scan without applying changes | **Audit** | Report problems and next decisions only; do not emit Naming decisions as if terms were adopted |

Disambiguation:

- **Verify** = “are these chosen terms acceptable?” (decision check).
- **Audit** = “what naming problems exist in this scope?” (opportunity inventory).
- Phrases such as “naming review” alone are ambiguous: if the user points at specific terms or “adopted / selected / 採用” language, use **verify**; if they ask what is wrong or what could improve, use **audit**; if they authorize fixes, use **improve**.

When the request is still ambiguous, use embedded mode if it authorizes a change; otherwise ask which of verify or audit they want—do not guess mutation.

## Apply The Scope Gate

### Fire The Full Workflow When

All of the following hold for a name:

1. **Mutation or check intent:** the task introduces, renames, repurposes, translates, abbreviates, broadens, narrows, or—under verify—re-checks the term.
2. **Not exempt** under [Exemptions](#exemptions).
3. **Non-trivial:** at least one of:
   - the name is or will be **shared** or **public** vocabulary (see surface classes below);
   - a **semantic choice** exists (two serious candidates, or a new term vs an existing adjacent term);
   - the name is a **domain term** (ubiquitous-language candidate) used in product, ops, or model speech;
   - the same spelling will be read **outside one obvious expression or tiny local scope** (other functions, modules, tests, docs, or configs).

If the full workflow fires for one or more terms, emit **Naming decisions** for exactly those terms. Do not emit rows for exempt names.

### Exemptions

Do not require candidate comparison or Naming decisions rows for:

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

- **local:** reversible implementation detail.
- **shared:** repository-wide or bounded-context language used by multiple components or documents.
- **public:** API, schema, wire format, event, CLI, configuration, telemetry, serialized data, database, or another externally consumed contract.

Treat public renames as compatibility and migration work, even when the surface is labeled experimental.

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

Read [references/calibration.md](references/calibration.md) when candidates remain close, when auditing, or when evaluating this skill. The calibration comparison is a **working** tool for choosing; it is not the final report.

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

For local decisions, proceed without waiting. For shared vocabulary, update an existing glossary or domain document when the repository has one. Do not create a glossary solely to record one obvious term.

For public changes, identify consumers and establish the safe path: preserve the current name, add a compatible alias, deprecate it, version the contract, or migrate consumers and stored data. Ask before proceeding only when the required compatibility strategy is not already authorized or discoverable.

In verify mode, skip implementation unless the user asks to apply fixes.

### 8. Verify The Vocabulary

Search again for:

- the previous term and spelling;
- rejected synonyms and abbreviations;
- conflicting uses of the selected term;
- callers, consumers, fixtures, snapshots, generated artifacts, and migration code;
- documentation or telemetry that still teaches the old vocabulary.

Run the relevant tests and compatibility checks. A passing test suite does not by itself prove that the vocabulary is coherent.

### 9. Emit Naming Decisions

In the final response, report every in-scope non-exempt term using the contract in [references/naming-decisions.md](references/naming-decisions.md).

Rules that keep cognitive load low:

- one table (or one single-term card) for all terms; public rows first, then shared, then local;
- required columns: Id (`n1`, `n2`, …), Term, Definition, Use site, Rejected (why), Surface, Compat;
- assign Id after sort, starting at `n1` in each block, so the user can type short references (`n2が微妙`);
- in verify mode, add Status (`OK` / `RISK` / `REJECT`);
- ban process narrative, search logs, file dumps, and dual prose restatement of the table;
- omit exempt names entirely.

Place the block where a reviewer will see it without mining the transcript—normally at the end of the final response, or as the whole response in verify mode.

## Handle Audit Mode

Audit only the scope the user names. Report each consequential issue with the current term, observed meaning, evidence from use sites, conceptual conflict, affected surface, and recommended next decision. Include safe counterexamples so the report does not become a blanket style critique.

Do not edit in audit mode. Do not present audit findings as Naming decisions. If the user later asks to apply a finding, switch to improve mode for that scope without repeating the full audit.

## Escalate Only At Contract Boundaries

Ask the user only when:

- the domain evidence supports multiple materially different definitions;
- the change would merge or split established concepts;
- a public rename lacks an authorized compatibility strategy;
- resolving the name requires an API, schema, permission-boundary, or other structural expansion outside the task.

Present the competing definitions, strongest candidates, consequential difference, and migration impact. Do not ask the user to choose between names without this evidence.

If a Naming decisions row cannot be completed (no definition, no use site, or unresolved public compat), that is an open decision—not a finished adoption.

## Definition Of Done

Do not finish a task that fires the scope gate until:

- the selected term has a one-sentence definition with context and exclusions;
- an important alternative has been compared and rejected for a concrete reason (when a genuine choice existed);
- representative declarations and use sites have been inspected;
- the selected term has been propagated across affected surfaces (embedded and improve modes);
- stale and competing terms have been searched again;
- compatibility impact has been handled or explicitly reported;
- **Naming decisions** has been emitted for every in-scope non-exempt term per [references/naming-decisions.md](references/naming-decisions.md).

Omit Naming decisions only when the scope gate does not fire (every name is exempt or no naming work occurred).

## License And Attribution

This skill is an adaptation of `evolutionary-naming` by kawasima. See [ATTRIBUTION.md](ATTRIBUTION.md) for the source, license, upstream notices, and a description of the changes. This skill directory is licensed under [CC BY 4.0](LICENSE).
