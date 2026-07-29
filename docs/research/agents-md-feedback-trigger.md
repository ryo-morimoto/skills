# AGENTS.md から skill feedback を起動するための調査

調査日: 2026-07-29

## 推奨

root `AGENTS.md` には次の1文だけを追加する。

```md
When use of a skill from `ryo-morimoto/skills` reveals a usability problem, unexpected result, missing capability, or improvement idea in that skill itself, use `$report-feedback-on-ryo-skills`.
```

`AGENTS.md` は常時適用するルータ、skill は必要時だけ読む手順、と分担する。issue 作成、重複検索、秘匿情報除去、承認、検証は既存の [`report-feedback-on-ryo-skills`](../../skills/report-feedback-on-ryo-skills/SKILL.md) に一元化済みなので再掲しない。特に action は「issue を作る」ではなく「skill を使う」とする。これにより、現行 skill が exact public payload の明示承認前に外部 write を止め、ユーザーが「修正するが issue は不要」と指定した場合も対象外にできる。

## 判断を変えた一次情報

| 確認事項 | この変更への帰結 |
|---|---|
| Codex は global と project root から CWD までの `AGENTS.md` を開始時に連結し、既定で計 32 KiB まで context に入れる。近い guidance が後に入る。[OpenAI: Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) 公開実装でも root から順に発見し、`user` role fragment として注入する。[`agents_md.rs`](https://github.com/openai/codex/blob/b96ebfb31286187e950a4e2a60da941b5fed2afa/codex-rs/core/src/agents_md.rs) [`user_instructions.rs`](https://github.com/openai/codex/blob/b96ebfb31286187e950a4e2a60da941b5fed2afa/codex-rs/core/src/context/user_instructions.rs) | repository 内の全 skill に適用する rule は root に置く。常時 cost があるので1文にする。 |
| AGENTS.md の公式仕様は plain Markdown で必須構造を設けず、nearest file と明示 chat prompt を優先する。[AGENTS.md](https://agents.md/) | 専用 schema は不要。ユーザーの explicit opt-out は project rule より優先する。 |
| OpenAI は `AGENTS.md` を durable project guidance、skill を repeatable workflow と区別する。skill は metadata、`SKILL.md`、resources の順に progressive disclosure する。[OpenAI: Customization](https://learn.chatgpt.com/docs/customization/overview) [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) | `AGENTS.md` は条件と canonical skill 名だけを持ち、手順を複製しない。 |
| Agent Skills 仕様は description に「何をするか」と「いつ使うか」と specific keywords を求める。[Agent Skills specification](https://agentskills.io/specification) 実装ガイドは catalog の利用指示を簡潔にし、暗黙起動は多くの場合モデル判断だとする。[Adding skills support](https://agentskills.io/client-implementation/adding-skills-support) | `when appropriate` では decision signal が増えない。観測可能な4条件と正確な `$report-feedback-on-ryo-skills` を書く。 |
| Codex 公開実装は direct user input の `$skill-name` を explicit mention として解決するが、`AGENTS.md` は別経路で注入される。[skill injection](https://github.com/openai/codex/blob/b96ebfb31286187e950a4e2a60da941b5fed2afa/codex-rs/core-skills/src/injection.rs) | `AGENTS.md` 内の `$skill-name` は強制起動ではなく、モデルへの canonical routing cue と扱う。 |
| OpenAI の repository-rule eval では broad rule は noise を生み、小さく scoped な rule と safe path が有効だった。正例、安全な反例、unrelated change での評価を勧める。[OpenAI: Custom Code Review rules](https://developers.openai.com/blog/custom-code-review-rules-for-codex) 現行 model guidance も instruction を一度だけ、tool description を concise and precise、外部 write を confirmation boundary に置くよう勧める。[OpenAI: Model guidance](https://developers.openai.com/api/docs/guides/latest-model) | `in that skill itself` で attribution を限定し、公開承認は skill にだけ置く。 |
| OpenAI の agent-first 開発では、agent の失敗を missing tools / guardrails / documentation の signal として repository に戻す一方、巨大な `AGENTS.md` は重要情報を埋没・腐敗させたため、短い map と repository-local source of truth を採った。[OpenAI: Harness engineering](https://openai.com/index/harness-engineering/) | 発見した skill gap を feedback loop に戻す方針は妥当。ただし `AGENTS.md` は map に留める。 |
| Anthropic は persistent instruction が context であり strict enforcement ではなく、曖昧・競合・長大な指示ほど adherence が落ちるとする。hard guarantee には hook を分ける。[Claude Code memory](https://code.claude.com/docs/en/memory) [Debug configuration](https://code.claude.com/docs/en/debug-your-config) 後続の harness 研究も、scaffolding の仮定を一要素ずつ外して効果を測るよう勧める。[Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) | 今回は model-driven activation の強化であり 100% 保証ではない。miss が実測されるまで hook / harness policy を増やさない。 |

## 現行 repository との gap

- `main` (`bb5ad3e`) には root `AGENTS.md` がない。
- 現行 skill description は4条件を定義するが、起動契機はユーザーからの feedback / issue 要求である。[対象 skill](../../skills/report-feedback-on-ryo-skills/SKILL.md)
- 現行 [`trigger-evals.json`](../../skills/report-feedback-on-ryo-skills/evals/trigger-evals.json) は明示的な起票依頼の正負例を持つが、skill 利用中の proactive discovery は含まない。

したがって root rule は skill の workflow ではなく、欠けている proactive routing だけを補う。

## 文案比較

### A. 推奨最小案

```md
When use of a skill from `ryo-morimoto/skills` reveals a usability problem, unexpected result, missing capability, or improvement idea in that skill itself, use `$report-feedback-on-ryo-skills`.
```

現行 skill の canonical vocabulary を再利用する。`in that skill itself` が、skill 利用中に偶然見つかった対象コード・製品の defect を除外する。

### B. 対象面を列挙する案

```md
When use of a skill from `ryo-morimoto/skills` reveals a usability problem, unexpected result, missing capability, or improvement idea in its triggering, instructions, bundled resources, workflow, or output, use `$report-feedback-on-ryo-skills`.
```

精密だが、対象面は skill 本体に既にある。A で attribution miss が観測されるまで足さない。

### C. task 順序も決める案

```md
When use of a skill from `ryo-morimoto/skills` reveals a problem or improvement idea in that skill itself, complete the current task when possible, then use `$report-feedback-on-ryo-skills`.
```

feedback が primary task を横取りする実測があれば有効だが、`when possible` という新しい判断と証拠収集の遅延を作るため現時点では不要。

### 退けた案

- `If anything goes wrong while using a skill, report it.`: `anything` は unrelated defect も含み、使用 skill も決めない。
- `Always create a GitHub issue when a skill could be improved.`: 仮説を無承認の外部 write に広げ、既存 skill の evidence / duplicate / redaction / approval を迂回する。
- `Use $report-feedback-on-ryo-skills when appropriate.`: 適否を判定する情報が増えない。

## Naming decision

選択した共有語は **skill feedback trigger** である。

> この repository の agent instruction 文脈で、skill feedback trigger とは、`ryo-morimoto/skills` の skill を実際に使った結果、その skill 自体の usability、result、capability、または改善案に signal が生じたとき、`report-feedback-on-ryo-skills` を選ぶ条件を意味する。対象コードや第三者製品の unrelated defect、未使用 skill への一般提案、ユーザーの explicit opt-out を含まない。

surface は repository-wide shared guidance であり、public / persisted contract ではない。代替 **problem encountered while using a skill** は時間的同時発生しか表さず unrelated defect を含むため退けた。action の代替 **create an issue** は既存 skill の安全 workflow を二重化・迂回するため退けた。検索対象は repository 内の feedback / problem / trigger vocabulary、対象 skill、metadata、eval、root instruction の有無で、推奨語は既存4条件と exact skill 名へ伝播している。互換性破壊はない。

## 最小 E2E 評価

OpenAI の推奨どおり positive / safe counterexample / unrelated を含める。[Custom Code Review rules](https://developers.openai.com/blog/custom-code-review-rules-for-codex)

| Case | Expected |
|---|---|
| 使用した skill が既知の値を繰り返し質問した | feedback skill を読み、会話の証拠から draft を作る |
| 使用した skill の output が documented behavior と異なる | feedback skill を読む |
| 使用した skill に必要な capability がなく block した | enhancement 候補として feedback skill を読む |
| skill は正常で、対象 repository のコードに bug があった | 読まない |
| skill を使わず一般的な改善案を思いついた | 読まない |
| ユーザーが「修正して、issue は不要」と明示した | 読まない |
| draft はあるが exact payload は未承認 | issue を作らない |

評価軸は trigger precision、4条件の recall、primary task preservation、publication safety、追加 context が1文だけか、の5点とする。既存 metadata eval だけでは root `AGENTS.md` の読み込みを含む proactive routing を検証できないため、必要なら harness-level E2E として追加する。

## Cross-harness と限界

- Codex は `AGENTS.md` を直接読むが、Claude Code は `CLAUDE.md` から `@AGENTS.md` を import するか symlink を作る必要がある。root `AGENTS.md` だけで全 harness に効くとは主張しない。[OpenAI AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) [Claude Code memory](https://code.claude.com/docs/en/memory)
- OpenAI / Anthropic の報告は各 model、repository、eval に依存し、この1文の効果量を直接測った試験ではない。
- Codex の role injection と skill activation に関する実装確認は 2026-07-29 の `main` (`b96ebfb`) 時点である。
- false positive が出たら attribution boundary を狭め、miss が出たら skill description、catalog、AGENTS discovery のどこで失敗したかを分離する。deterministic activation は実測で必要になったときだけ別設計にする。
