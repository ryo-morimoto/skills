# Naming As Design Evidence

Read this reference when precise naming exposes mixed responsibilities, an unstable boundary, or a missing domain abstraction. Do not read it for every routine local name.

## Diagnose The Signal

| Signal | Likely design problem | Investigation |
|---|---|---|
| An honest name lists several unrelated actions | Mixed responsibility | Identify independently changeable effects and consumers |
| The definition changes across call sites | Misplaced abstraction or multiple concepts | Group call sites by intended meaning and bounded context |
| The same context must be repeated in every name | Wrong owner or module boundary | Find the receiver or namespace that should supply the context |
| Parameters or fields repeatedly travel together | Missing whole value or domain object | Define the invariant that binds the values |
| Many synonyms represent one concept | Missing canonical vocabulary | Select the established term and migrate the rest |
| One term represents several concepts | Semantic collision | Split meanings or qualify them by bounded context |
| A name describes timing such as `onLoad` | Invocation detail replacing intent | Identify the state transition or outcome callers need |
| Only broad nouns or verbs seem possible | Domain knowledge or responsibility is incomplete | Inspect behavior, effects, preconditions, and outcomes |

## Choose The Smallest Structural Response

Use the smallest change that makes an honest name natural:

1. Extract a local expression or function when one operation lacks a name.
2. Split a function or type when an honest name must enumerate independent responsibilities.
3. Move behavior to a receiver or module that supplies repeated context.
4. Introduce a value object when values travel together under one invariant.
5. Separate bounded contexts when one word cannot retain one meaning.
6. Add an explicit state or transition when vague verbs hide lifecycle semantics.

Do not shorten the name first. Let the awkward honest name expose the boundary, improve the structure, and then name each resulting responsibility by its intent.

## Preserve Authorization And Behavior

- Apply a small structural correction when it is inside the user's task and preserves the existing contract.
- Ask before expanding into an unrequested API, schema, persistence, permission, or cross-service change.
- Keep behavior-preserving renames separate from behavioral changes when practical.
- Run focused tests after structural changes and compatibility checks after contract changes.
- Do not force a domain abstraction without evidence from invariants, call sites, or domain language.

## Re-evaluate At Use Sites

After the structural response:

1. Re-read representative callers without relying on the implementation body.
2. Confirm that each name communicates why the operation exists, not merely how it works.
3. Confirm that the same term retains the same meaning across code, tests, contracts, and documentation.
4. Search for the broad or conflicting term that revealed the problem.

If the new structure still requires an unstable or misleading name, the design issue remains unresolved.
