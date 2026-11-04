# Independent critique

criticは別contextで全案を同じ条件で読む。採点多数決や合成の担当ではない。
`design-evaluation.md` を読み、案間の実質差と各案の妥当性を別の評価として実施する。
`planning-modes.md` に従い、最低3変更候補と領域coverage、併用条件を確認する。
差があることを妥当性の証拠にせず、妥当であることを別案の証拠にしない。

## Checks

1. alternativesは同じ目的・scope、portfolioは共通の全体条件と明示した領域別目的で比較しているか。
2. 責務・所有権・依存・移行の実質差があるか。単なる言い換えではないか。
3. authored callers、エラー、副作用、権限、データ、配布境界を落としていないか。
4. 移行途中の稼働状態、共存、検証、廃止条件、rollback/forwardが具体的か。
5. 工数にテスト・調整・共存・廃止が含まれるか。効果開始の遅れを扱ったか。
6. 根拠・仮定・未知が区別され、便益・cost・risk penaltyが二重計上されていないか。
7. gate、重大リスク、回復不能性を便益で相殺していないか。
8. 実行していないことをpassと報告せず、人間が選択できる粒度か。

## Findings

- `blocking`: 比較自体が成立しない、必須契約違反、根拠捏造、重大な未説明の危険。
- `major`: 推薦を変え得る重要な不足・楽観。条件付きか修正が必要。
- `minor`: 主判定を変えない説明・表記の改善。

各指摘にplan ID、根拠ID、具体的issue、修正方法を付ける。
実行で証明できない予測リスクを、それだけで棄却しない。
大きな修正で計画が変わったらplan revisionを上げ、元批評の適用範囲を残す。
親は解決済み指摘と残る不一致を区別し、一回で解決しなければ無理に収束させない。

## Required design evaluation

新規出力は `critique_result.design_review` に全変更案ペアとP0を含む全案の評価を
持つ。六criterion・判定・成立条件・根拠は `design-evaluation.md` に従う。
`findings` が空でも、評価を省略したことと「妥当性を確認したこと」は区別する。
invalidは推薦不可、conditional/unknownは条件付き。duplicateは別案数に含めないが、
同じ設計であることだけを理由に個々の設計をinvalidにしない。
