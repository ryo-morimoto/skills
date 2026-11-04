# Three-or-more candidates and area portfolios

## Count honestly

変更候補を**最低3案**生成する。P0は別枠であり、「P0＋2案」を三案と数えない。
既定は3案だが上限3案ではない。領域数・依頼・予算に合わせて増やす。
同じ案の改名、弱い案や全面rewriteの強制追加、工程分業を候補数へ水増ししない。
初回は候補ごとに独立contextのplannerを最低3つ同一batchで並列起動する。

三つの妥当な案が必ず存在するとは限らない。調査した不成立案は残し、
「検討した候補数」「成立候補数」「実質差を確認できた数」を区別する。
3候補未提出なら不足を明示した途中報告とし、完成packetを捏造しない。
同じscopeで三つの実質案がない場合、勝手に領域やscopeを拡張しない。

## Pick the decision mode, not a fixed three-way contrast

| mode | 人間の問い | 案の関係 | 出力 |
|---|---|---|---|
| alternatives | この対象をどう直すか | 同じ目的・対象への代替方針 | 3案以上＋P0、選択を変える差と成立条件 |
| portfolio | どの領域を何から直すか | 領域別に独立・併用・依存・競合し得る改善候補 | 3候補以上＋P0、領域coverage、併用条件と順序 |

明示された依頼を優先する。広い範囲の「改善候補を洗い出して」「領域ごとに比較」なら
portfolio、特定問題の「方式を比較」ならalternativesを選び、最初にmodeを説明する。
判断が曖昧で選択を変える場合だけ質問する。単に3案を作るためにmodeを変えない。

## Area discovery

コード・caller・契約・変更伝播から領域を定義する。例えば業務ルール、永続化境界、
外部連携、UI状態等。ただし固定の三領域を毎回押し付けない。
directoryを三つ見つけたことだけを改善案にしない。同じfileに複数の責務があってもよい。
各領域に対象scope、目的、成功scenario、現状の具体的な問題・根拠を付ける。
関連のない機能追加やテスト担当を、領域別リファクタと称さない。

portfolioでは全体目的・保存契約・期間は共通とし、各候補は担当領域の目的に対応する。
一案で全領域を解決する必要はない。選んだ領域には各1候補以上、全体で最低3候補。
これは「全領域に自動的に3案ずつ」を意味しない。領域内の方式比較も必要なら、その領域に
代替3案以上を生成し、同一領域内の競合と領域間の組合せを別々に表示する。
予算で未調査の領域を黙って落とさず、contextのnon_goals/unknownsに理由と判断影響を残す。

領域plannerも完全な計画（before/after、caller、移行、検証、回復、費用・効果・未知）を返す。
「Aが調査、Bが実装、Cがtest」という単一計画の工程分業ではない。

## Planning contract — new packets use schema 1.1

`planning` に次を明示する。型の正本は同梱schema、旧1.0は履歴読込み専用。

- `mode`: alternatives / portfolio。
- `areas`: id、name、scope、objective、success_scenarios。
- `assignments`: plan_id、area_ids、depends_on（候補IDの前提依存）。P0は割り当てない。
- `relations`: 全変更候補ペアのplan_ids、relationship、compatibility、benefit_overlap、reason、evidence_ids。

relationshipは `alternative / complementary / independent / unknown`。
compatibilityは `compatible / conflicting / unknown`。
benefit_overlapは `disjoint / shared / unknown`。共有fileの衝突、同じcallerや変更scenario、
共通の前提作業や便益の二重計上を検査する。領域が違うだけで独立・便益非重複と認定しない。
depends_onはplan単位の有向DAGであり、各plan内部のstepsとは別。
criticが全ペアの関係・方向・根拠を確認する。両立しない候補は同時採用しない。

alternativesは一対象のareaとし、同一scope・目的の三つ以上の方式を比較する。
portfolioは最低二領域とし、担当scopeが違うこと自体を不当比較としない。
ただし領域内の代替案は同じ成功scenarioで比較する。
全ペアのdesign_reviewも維持し、別領域のdistinctを「同じ問題の代替が三つ」と言い換えない。

## Compare without fake equivalence

各領域でのbefore/after、代表変更、残存負債、目的指標、依存・回復を比較する。
人時に換算できなければ原単位とunknownを残す。「file数」「抽象化の数」だけで順位を決めない。
共通horizonでも、目的・露出頻度・受益者が違えば単一の効果スコアにはならない。

portfolioの候補間に投資回収の交点を計算して「こちらが勝つ」としない。
P0との差分は候補単体の仮定として表示できるが、セット採用時の便益・費用を単純加算しない。
重複する作業・便益、依存実装、相互作用、同時担当の能力、便益開始のずれを別途再見積する。
初版portfolio計算器は組合せの総額・総便益を自動算出しない。

priorityは目的への寄与、必須期限、先行依存、回復可能性、証拠の成熟度に基づく条件付きの
着手順として説明する。非重複性不明ならunknown、判定不能なら保留する。
多くの領域を触る案や、見積が安く見える案を自動的に優位にしない。

## Human decision

alternativesは一つのplan_id、portfolioはplan_id:nullとplan_ids配列を使う。
portfolioは複数採用・一部採用・保留を表せる。前提候補を含め、競合する組合せを選ばない。
未知の併用条件は条件として残し、安全なセットと断言しない。
推薦は回答ではない。実際の回答までpending、選択後も実装しない。
