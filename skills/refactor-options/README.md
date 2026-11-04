# refactor-options

目的に対して最低3つのリファクタ候補を独立に並列検討し、人間が選べる比較資料を作るskill。
費用・リスク・インパクトだけでなく、案間の実質差と各案の設計妥当性を評価する。
**計画・意思決定支援のみ。選択後も実装を開始しない。**

## Use

このdirectoryを利用するhostのskill探索先へ配置するか、そのhostのskill installerを使う。
`SKILL.md` が入口。独立contextのplannerを最低3つ同時起動でき、その後に別criticを
起動できるhostと、Python 3.10+が必要。能力・権限が不足すればblockedで停止する。

```text
$refactor-options
注文処理の変更負担を減らしたい。
領域ごとの改善候補を最低3つ出し、併用条件と着手順を比較してください。
公開APIと失敗時の挙動を維持し、まだコードは変更しないでください。
```

hostによって明示呼出しの表記は異なる。配置や発見だけではscriptは実行されない。
制約がhost強制か指示ベースかを明示し、このskill自体をsandboxとは扱わない。

## Two planning modes

| mode | 比較するもの |
|---|---|
| alternatives | 同じ対象・目的への方式を最低3案。P0は別枠 |
| portfolio | 各領域の完全な改善計画。全体で最低3候補、対象領域ごとに最低1候補 |

特定領域内の方式比較も依頼された場合は、その領域でも3方式以上を検討する。
上限3案ではない。改名・工程分業・P0で数を水増しせず、候補数・実質差・妥当性を区別する。
条件内で十分な案を示せなければ、未充足として報告する。

portfolioは前提依存・併用可否・便益重複を全ペアで確認する。複数／一部採用や保留を表せるが、
領域名が違うだけで独立とは認定しない。セットの費用・便益を単純加算せず、勝者を強制しない。

## Package

- `SKILL.md` / `references/`: workflow、mode、根拠・見積・設計評価、planner/critic prompts。
- `assets/`: schema、表示template、完全に架空の型・算術例。
- `scripts/compare.py`: stdin/stdoutだけの検査・計算・表示。Python標準ライブラリのみ。
- `tests/`: 計算器・schema・CLI・package・eval定義の静的検査。
- `evals/`: 4つの基本ケースと13の追加ケース、入力fixture、判定基準。
- `agents/openai.yaml`: 対応host向けの表示名と呼出し例。

新規packet/contextはschema 1.1。旧1.0は履歴読込み用であり、2案の例を現行最低数へ転用しない。
design-reviewとformulaのversionは1.0。invalid案は除外し、conditional/unknownは条件を残す。
plausibleは静的な計画の筋であり、実行時の正しさ・安全性や経済性の保証ではない。

## Development checks

このリポジトリのrootから:

```sh
python3 -B -m unittest discover -s skills/refactor-options/tests -v
python3 -I -B skills/refactor-options/scripts/compare.py validate --type decision_packet < skills/refactor-options/assets/example-portfolio.json
```

これは同梱計算器と定義の検査であり、対象アプリやfixtureの実行ではない。
公開packageには245のunit checksがあり、ローカル評価履歴にだけ依存する1件は履歴未同梱ならskipする。
evalのモデル実行成功と、unit checksの合格を混同しない。

[evalケース一覧・実行境界・採点方針](evals/CASE-SUITE.md) · [計算器の契約](scripts/README.md)

## Publication boundary

この公開packageにはskill本体、同梱計算器、tests、架空fixtureとeval定義だけを含める。
ローカル実行結果・会話trace・machine paths・認証設定・waxa等の導入物や試行runner・
元プロジェクトの調査資料は含まない。結果は利用者の環境で取得し、公開時は別途内容を確認する。
`evals/results/` 等は追跡しない。通常利用でtestsやevalsを実行する必要はない。
