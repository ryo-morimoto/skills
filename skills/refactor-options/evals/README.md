# Refactor options — evaluation definitions

このdirectoryにはモデル評価用のcase foldersと架空入力を置く。
caseの定義・静的形式検査・実際のモデル評価結果は別物であり、実行済みの合格率を含まない。
ローカルの会話trace、実行結果、認証設定、導入済みtoolや試行runnerは公開packageに含めない。

## Basic cases

| case | 内容 |
|---|---|
| local-boundary | 小さな税率重複に対する方式比較、契約・移行・回復・未知 |
| parallel-unavailable | 並列subagent等の権限がない場合のblocked |
| three-alternatives | P0を除く最低3方式、全ペアの差と個別設計の妥当性 |
| area-portfolio | 価格・永続化・通知の領域別候補、共有file・副作用・便益重複 |

## Additional suite

[CASE-SUITE.md](CASE-SUITE.md) に13追加ケース／39判定基準の一覧と実行・採点方針を示す。
`case-suite.json` は定義のindexであり、runner adapterや評価結果ではない。

```text
evals/<case-name>/
  prompt.md
  case.yaml
  graders/*.md
  files/*          # 入力が必要なケースのみ
  place-files.sh   # host準備用。被評価agentへ実行許可を与えるものではない
```

被評価agentにはpromptとそのケースの入力だけを渡し、graders・過去結果は見せない。
generationには最低3つの新contextの同時起動と独立criticが必要。review/capability/lifecycleは
対応工程だけの試験であり、その合格を自律生成や並列実行成功とは呼ばない。

実行する場合はこのskill内の `evals/results/` の新しいiterationに保存する。
そこはGit除外対象であり、未確認の出力やtraceを公開しない。
公開packageのunit checksはモデル・fixtureを実行しない。scope-injectionの補助scriptも実行しない。
