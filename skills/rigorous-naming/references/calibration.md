# Naming Calibration

Read this reference when candidates remain close, when performing an audit, or when evaluating whether the skill is too strict or too permissive.

## Rank Candidate Qualities

Evaluate candidates in this order:

1. **Truth:** Does the name describe behavior and state that actually exist?
2. **Boundary:** Does it include the intended cases and exclude adjacent concepts?
3. **Use-site clarity:** Does it express intent naturally where callers read it?
4. **Vocabulary coherence:** Does it preserve the bounded context's canonical language?
5. **Contract stability:** Will consumers interpret it consistently over time?
6. **Brevity:** Is it no longer than the context requires after the higher priorities are satisfied?

Do not average these into a cosmetic score. A failure in truth, boundary, or contract stability disqualifies a candidate.

## Compare Candidates

Use a compact comparison when the choice is consequential:

| Candidate | Exact definition | Reads at use sites | Conflicts or synonyms | Compatibility |
|---|---|---|---|---|
| `<candidate A>` | `<fit or mismatch>` | `<representative example>` | `<existing language>` | `<impact>` |
| `<candidate B>` | `<fit or mismatch>` | `<representative example>` | `<existing language>` | `<impact>` |

The comparison exists to expose meaning, not to manufacture ceremony. Stop after the decisive difference is visible.

After the choice is made, do not paste this matrix into the final response. Emit **Naming decisions** per [naming-decisions.md](naming-decisions.md) instead—one rejected alternative is enough there.

## Positive And Negative Examples

- Reject `processData()` when the subject, transition, and outcome are unknown. Prefer `captureAuthorizedPayment()` only when it truthfully describes the precondition and outcome.
- Reject `returnsCorrectResult` because `correct` delegates the assertion to the reader. Prefer an observable claim such as `rejectsExpiredAccessToken`.
- Accept `invoice.total()` when the receiver supplies the context. `calculateInvoiceTotal()` repeats information without adding meaning.
- Accept `i` in a short conventional loop whose scope fully constrains it.
- Preserve framework and protocol names when their canonical meaning is intended.
- Do not mechanically replace public `userId` with `accountId`. Establish whether user and account are identical concepts and define the migration first.
- Do not reject `Manager`, `Data`, or `Info` by spelling alone. Reject the candidate when its definition is broad, unstable, or inconsistent with use sites.

## Detect False Improvements

Reject a rename that only:

- substitutes a fashionable synonym;
- shortens an honest name while hiding behavior;
- repeats the type or receiver without distinguishing the instance;
- translates one surface while leaving code, tests, events, or docs on the old vocabulary;
- changes an internal identifier while silently changing a wire or persisted name;
- makes a test sound fluent without making the observed behavior explicit.

## Test Restraint

Include these negative fixtures when evaluating the skill:

- a generated file;
- a framework callback with a prescribed name;
- an established industry term used canonically;
- a tiny loop variable;
- an unrelated value-only change;
- a local rename whose exact canonical replacement is already established.

The skill should avoid extra candidates, questions, and refactoring in these cases.
