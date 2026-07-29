# Research: Adoption Review for Rigorous Naming

Research date: 2026-07-29  
Scope: design basis for a **batch-reviewable, low-cognitive-load** presentation of adopted names.  
Not an implementation. Synthesis is labeled as inference; primary claims keep source attribution.

## Problem statement

`rigorous-naming` already requires a Definition of Done and a final report:

> selected term and definition, rejected alternative and reason, searched or updated surfaces, and compatibility impact

Gaps observed:

1. The report is free-form. Multiple adopted names cannot be scanned as one set.
2. Agents often bury the decision in process narrative, or omit fields.
3. Reviewers must reconstruct "is this name OK?" from long text, which raises cognitive load—the user's dominant constraint across sessions.

Design goal: after a task (or on demand), show **only the fields a human needs to accept or reject each adopted term**, in a scannable batch form.

---

## Evidence sources

### A. Web / primary literature

| Source | Relevant claim | Design use |
|---|---|---|
| [Sweller, Cognitive Load During Problem Solving](https://doi.org/10.1016/0364-0213(88)90023-7) | Limited working memory; means-ends noise blocks schema use | Delete process narrative and non-decision fields from the review surface |
| [t-wada, テストコードの認知負荷 (gihyo / WEB+DB PRESS)](https://gihyo.jp/dev/serial/01/savanna-letter/0007) | Both **too little** and **too much** information raise load; keep intent-critical facts, strip irrelevant ones | Adoption card must include definition + use-site evidence, exclude search logs and file dumps by default |
| [Evans / Fowler, Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html) | Language must be rigorous (software rejects ambiguity); experts reject awkward terms; developers watch inconsistency | Definition with includes/excludes is mandatory; synonym proliferation is a defect |
| [Evans DDD Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) | UL names classes, methods, rules; one model per bounded context | Surface classification (local / shared / public) and context binding |
| [Belshee, Naming as a Process](https://www.digdeeproots.com/articles/naming-process/) | Naming is design; honest→complete→intent; judge names where callers read them | Use-site example is non-optional for validation |
| [kawasima evolutionary-naming audit table](https://github.com/kawasima/evolutionary-naming) | Phase-grouped tables for scan; stop after classification; no silent refactor | Batch table > prose; group by review cost / permission, not by file |
| [Nygard ADR](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | Short Context / Decision / Consequences; one decision per record; large docs are unread | One row/card per term; decision first; consequences = compatibility + vocabulary impact |
| [Code Review Pyramid (Morling)](https://www.morling.dev/blog/the-code-review-pyramid/) | Reviewers waste focus on low-value style; automate bottom, focus top | Human review surface focuses on meaning/boundary/contract, not casing style |
| [Cisco / later changeset-size review research](https://rishi.baldawa.com/posts/pr-throughput/cognitive-load-cliff/) | Defect detection collapses with large review units | Prefer many tiny name cards over one wall of mixed renames |
| [distill-decision-signal research-basis](../distill-decision-signal/references/research-basis.md) (in-repo sibling skill) | Information bottleneck + value of information: keep only what changes the decision; frontload result | Counterfactual deletion test for every field on the card |
| [GOV.UK / ONS content design](https://service-manual.ons.gov.uk/content/writing-for-users/structuring-content) | Inverted pyramid; must-have vs supporting vs optional | Default card = must-have only; expand on demand |

### B. Claude session history (user values)

Recurring user signals (Claude `history.jsonl` and project transcripts):

| Pattern | Example signal | Implication for adoption review |
|---|---|---|
| Cognitive load is primary | "認知負荷が高い", "技術的な認知負荷がオーバーして重要な要件が抜けている" | Review format is a product surface, not bookkeeping |
| Too little structure fails | ADR feedback: "何の課題・何を検討・何を優先・何にした" is thin when unsummarized | Card must force challenge → options → choice, not implementation diary |
| Too much structure fails | "無駄に長文", "情報はあるがまとまっていない", "わけすぎ" | Hard cap on fields; no process essay |
| Decisions must be findable | Final decisions left in comments are a load source (`ready-for-human` work) | Adoption summary lives in the **final response body**, not only tool traces |
| Scan-first UIs | "まとめて表示", "人間の認知負荷がないように html", dialogs rejected for bulk review | Batch table first; detail on expand |
| Vocabulary discipline | "存在しない語彙を追加しない", "余計な語彙を増やしてほしくない", Inventory≠ItemStock | Show **rejected synonym** and **existing domain term** when relevant |
| Naming vs glossary roles | "命名スキルは情報設計の観点、glossaryの案だしは別スキル" | Card is verification of a decision, not a full glossary workshop |

### C. Codex session history (skill origin + ops)

Key sessions:

- `019fa15c-…` (2026-07-27): research request—"語彙の追加や変更、命名には極端までに執着するルール"
- `019fa742-…` (2026-07-28): skill rename `design-names-and-vocabulary` → `rigorous-naming`, attribution, push of `bb5ad3e`
- `019fa2ab-…`: runtime friction—"Purchase ではなく BasCase", "語彙追加するときは許可", "新しいdomain語彙が必要になった場合は実装を停止し許可を得る" を不要にしたい

Design findings from those sessions:

1. **Completion evidence** was intentional: term + one-sentence meaning + rejected alternative + scope + compatibility.
2. Hybrid activation: AGENTS.md trigger + skill procedure (skill-only misses incidental naming).
3. Risk of **over-application** and ceremony was already known; exclusions and safe counterexamples were first-class.
4. Runtime pain is not "no report"—it is **hard to batch-verify** agent vocabulary choices, and agents still invent terms.

### D. Grok session log

Only the current session in `skills` workspace so far; this research is the first Grok pass on the improvement.

### E. Current skill assets

| Asset | Has | Lacks for adoption review |
|---|---|---|
| `SKILL.md` DoD / final response | Free-form four fields | Fixed scannable multi-term layout; severity; omit rules |
| `references/calibration.md` | Candidate comparison table; quality ranking Truth→…→Brevity | Human-facing **post-decision** card (after choice is made) |
| `references/design-signals.md` | When naming exposes design issues | How to surface a design-signal flag on the card without expanding into full design review |
| `evolutionary-naming` audit-mode | Excellent scan table for **problems** | Different job: scan **adopted decisions** for acceptance |

---

## Decision target (what the reviewer decides)

For each adopted term, the human answers one question:

> **Is this vocabulary choice acceptable to keep, or must it be reversed / escalated?**

Sub-judgments (only if the main answer is not automatic):

1. Is the meaning true and bounded (includes/excludes)?
2. Does it read honestly at a real use site?
3. Did we invent a synonym or collide with an existing term?
4. Is the contract surface risk handled?
5. Does the name expose an unresolved design smell that should stop progress?

Anything that does not change those judgments is noise.

---

## Field budget: counterfactual deletion test

| Field | If deleted, what fails? | Default |
|---|---|---|
| **Term** | Cannot identify the decision | Required |
| **One-sentence definition** (context + includes + excludes) | Cannot test truth/boundary (Evans UL, current step 2) | Required |
| **Use-site snippet** (1 line: call / access / test / error) | Cannot test honesty where readers live (Belshee, skill step 5) | Required |
| **Rejected alternative + one concrete reason** | Cannot detect fashion synonym / false improvement | Required for non-trivial choice |
| **Surface class** `local` / `shared` / `public-persisted` | Misjudges reversibility and risk | Required |
| **Compatibility** (alias / migrate / none / n-a) | Misses contract breakage | Required if public-persisted; else omit or `n/a` |
| **Design signal** (only if present) | Misses "honest name exposes bad structure" | Optional row flag |
| Search log / full file list | Rarely flips accept/reject once verification already ran | Omit from card; keep in agent notes if needed |
| Full multi-candidate matrix | Useful during choice; after choice only the decisive reject matters | Collapse to one reject |
| Process narrative ("I searched… then…") | Pure load | Ban on review surface |
| Casing / style notes | Automate elsewhere | Omit |

This matches t-wada: **enough for intent, nothing that forces the reader to filter**.

---

## Recommended review shapes (design candidates)

### Shape A — Batch decision table (default for 2+ terms)

```markdown
## Naming decisions

| Id | Term | Definition | Use site | Rejected (why) | Surface | Compat |
|---|---|---|---|---|---|---|
| n1 | `ItemStock` | Quantity record for an `Item`; excludes physical item identity | `item.stock.available` | `Inventory` — collides with RECORE vocabulary | public | wire unchanged |
| n2 | `BasCase` | In store ops, a buyback case; includes active intake, excludes inventory stock (`Item`) | `openBasCase(memberId)` | `Purchase` — invents non-domain synonym | shared | n/a |
```

- One row per adopted term.
- Empty optional columns stay empty or are dropped (no `—` ceremony columns).
- Sort: `public-persisted` first, then `shared`, then `local`.

### Shape B — Single-term card (1 term or escalation)

```markdown
### `ready-for-human`
**Means:** issue is dispatchable to a named human *now* (owner + action + exit evidence); not "any human interest".
**Use site:** label applied only when start conditions are satisfied.
**Rejected:** `human-attention-needed` — attracts passive waits.
**Surface:** shared workflow vocabulary.
**Compat:** label name kept; semantics tightened.
```

Maps cleanly to Nygard Decision + Context + Consequences without ADR ceremony for every local rename.

### Shape C — Audit of adoptions (explicit "まとめて確認")

When the user asks only to verify names already chosen (no edit):

```markdown
## Naming adoption review: <scope>

| Status | Term | Why |
|--------|------|-----|
| OK | … | definition matches use sites |
| RISK | … | public rename without migration |
| REJECT | … | synonym of established term |

### Needs decision
- …
```

Status column front-loads the human action (inverted pyramid).

### Shape D — Not recommended as default

- Long prose "Naming Report" with sections matching the 8 workflow steps.
- Exhaustive evolutionary-naming audit tables reused as adoption reports (wrong job: problem inventory ≠ decision verification).
- HTML dashboards unless multi-page bulk review is the task; markdown tables already match agent I/O.

---

## Interaction rules (to keep load low)

1. **Frontload the table** at the end of the task (or as the whole response in review-only mode). Do not open with search methodology.
2. **Omit exempt names** (tiny locals, prescribed framework names) entirely—current skill already says this; enforce it on the table.
3. **One reject is enough** after the choice; do not list three near-identical losers.
4. **No dual bookkeeping**: if the table is complete, do not also write a prose restatement of every row.
5. **Escalate only when the card cannot be filled** (undefined concept, concept merge/split, missing public migration)—same as current skill gates.
6. **Multiple terms → one table**, not N separate essays.
7. **Design signal flag** links to `design-signals.md` only when the honest name is still ugly; otherwise silence.
8. **Language**: match the user; definitions may be Japanese with English identifiers.

---

## Mapping to existing calibration order

Human scan order on the card should mirror calibration rank, not invent a new quality model:

1. Truth → definition sentence  
2. Boundary → includes/excludes in that sentence  
3. Use-site clarity → use-site column  
4. Vocabulary coherence → rejected synonym / existing term  
5. Contract stability → surface + compat  
6. Brevity → not a column; already decided if higher ranks pass  

---

## Synthesis: skill change directions (inference, not yet implemented)

| Change | Why |
|---|---|
| Add a named **Adoption Review** output contract (table/card) under DoD | Makes batch verification possible and field-complete |
| Specify **field budget** and ban process narrative on that surface | Cognitive load is the primary constraint |
| Add **review-only** trigger ("採用された命名を確認", "naming decisions") | Separates verification from implement/audit-improve |
| Keep comparison matrix in calibration for *choosing*; collapse after choose | Different jobs: decide vs verify |
| Sort by surface risk | Matches review pyramid / contract focus |
| Optional `references/adoption-review.md` with 2–3 positive/negative fixtures | Progressive disclosure; keep SKILL.md thin |
| Measure success as: reviewer time-to-judgment, missing-field rate, false synonym acceptance | Local kaizen metrics; not DORA |

Out of scope for this research:

- New glossary skill
- Linter for semantic truthfulness
- Forced human approval on every local name (contradicts current embedded mode)

---

## Open design questions — resolved (2026-07-29)

| Question | Resolution |
|---|---|
| Artifact name | **Naming decisions** — reports chosen terms; human uses the block to accept/reverse. Rejected `Adoption review` as the default heading (sounds like audit; reserved status language for verify mode only). |
| Use-site required? | Always. Declaration-only only when no other use site exists yet, and the row must say so. |
| Where it lives | Final chat response (end of task, or whole response in verify mode). No mandatory PR-body append. |
| Threshold | **Same as scope gate / fire condition.** Emit for every in-scope non-exempt term; omit when gate does not fire. |
| Relation to audit | **Verify** mode checks adopted terms; **Audit** inventories problems. Naming decisions is not used as an audit findings table. |

Implementation: `SKILL.md` + `references/naming-decisions.md`.

---

## Validity limits

- Session evidence is qualitative and biased to one developer's workflow (bookoff, skills, dotfiles).
- Cognitive-load literature is mostly learning/problem-solving; applying it to agent report design is synthesis.
- No A/B measurement yet of table vs prose on real tasks.
- Primary sources on naming (Evans, Belshee, Nygard, t-wada) support *what must be judged*, not a proven UI for agent skill reports.

---

## Primary links (quick index)

- https://gihyo.jp/dev/serial/01/savanna-letter/0007  
- https://martinfowler.com/bliki/UbiquitousLanguage.html  
- https://www.digdeeproots.com/articles/naming-process/  
- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions  
- https://www.morling.dev/blog/the-code-review-pyramid/  
- https://github.com/kawasima/evolutionary-naming  
- In-repo: `skills/rigorous-naming/SKILL.md`, `references/calibration.md`, sibling `distill-decision-signal`  
- Codex sessions: `019fa15c-efc7-7112-811e-b835eefd2271`, `019fa742-4a1f-7f61-86ce-688c075a678d`, `019fa2ab-532f-7223-8d31-7986ddfa3e4c`
