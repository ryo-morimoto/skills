# Cost, risk, and impact

数値は客観性の演出ではなく、前提と推薦の関係を調べるために使う。

## Shared range representation

rangeは `unit, low, reference, high, basis, evidence_ids, assumption_ids, reason`。
三点はすべて既知か、すべてnull。未知にはreasonが必要。
`reference` は基準scenarioで、中央値・期待値・P50ではない。
low/highも全可能性の境界や確率区間ではない。単位は比較前に揃える。

## Implementation cost

costsを、調査・設計、実装、回帰検証、caller移行、共存、廃止、調整・教育へ分解する。
`hours` のunitは `person_hour`。全案を同じ担当者像・AI支援条件で比較する。
未知componentを0にせず、既知小計と未見積を分ける。空のcostsは見積欠落である。
P0だけは「今回の追加投資なし」という明示的な0 componentを持つ。
LOC・file数×万能係数やcommit間隔から人時を作らない。
単価が提供された場合以外は金額へ変換しない。人時と暦日・外部待ちは別。
共通の未知が複数componentへ影響するなら整合したscenarioとして説明する。

## Impact and time

主指標は目的に対応させる。代表変更の人時、月削減人時、特定経路のlatency等。
coupling/churn/LOC等のproxyを開発速度や障害確率へ一律換算しない。
人時換算できない目的はbefore/afterや目的固有の単位で説明し、
`monthly_savings_hours` をunknownにする。無理に金銭評価へ変換しない。
portfolioは候補単体の共通基準に対する差分を記述し、受益者・代表変更・頻度の違いを残す。
領域間の容量差や回収交点だけで勝者を決めない。共有する作業・便益がある候補を組み合わせる
場合は再見積が必要で、単体cost/benefitをそのまま加算しない。
未調査の相互作用はunknownとし、未知のセット総額を既知小計から推測しない。

同じ評価期間H、完了月m、完了翌月から一定の月削減b、増分費用Cがある場合:

`net_capacity(H) = b * max(0, H - m) - C`

completionのunitは `month`、月削減のunitは `person_hour/month`。
固定費・共存費はcostsに一回だけ含める。この式に合わない漸進便益・段階別維持費は
当てはめず、適用外の未知として別scenarioを説明する。
初版のrange入力は非負であり、月次負担の増加を負の削減としては計算しない。
その場合は増加分を隠さず記述し、適用外として純削減計算を保留する。
余力削減は現金収入・人員削減・risk-adjusted ROIではない。
費用high、便益low、開始遅延を合わせた保守的scenario等を表示し、確率を与えない。

## Risk register

事象ごとに、原因→失敗→影響、migration/steady、検出、対策、回復、残余を記す。
`residual_severity` は発生した場合の影響で、発生確率ではない。

| S | 条件付き影響のanchor |
|---|---|
| 1 | 開発内部の局所手戻り。利用者・共有環境・データへ影響なし |
| 2 | 内部の単一利用経路の可逆な不具合。外部契約・永続データへ影響なし |
| 3 | 一部の利用者機能阻害または外部契約差。回復可能 |
| 4 | 基幹業務停止、独立配布領域への伝播、重大なデータ修復 |
| 5 | 回復不能な重要データ損失、重大漏えい・権限侵害、法令・安全上の重大影響 |

複数に該当すれば高い方。未知はnullと理由。計画上の対策は未検証と明示する。
発生しやすさだけを下げる対策ではseverityを下げない。
最大Sは特定済み事象についての情報で、空risk registerは安全の証明ではない。
回復の人時、影響範囲、確率の根拠不足は別に示す。
Sの平均・積、S4はS2の2倍、confidence4/5は成功率80%という換算をしない。

## Gates and conditional recommendation

constraintごとに `pass / fail / unknown`、理由、根拠を記す。
設計の整合と、将来の実行テスト成功を区別する。後者は未実施ならunknown。
failを高便益で相殺せず、unknownは条件付きとする。
全重要軸に根拠がない限り全軸でのPareto支配を断言しない。
生の序数を足す総合点は初版で提供しない。
期間・費用・頻度で推薦が変わる条件を返し、重要な未知が残れば保留する。
