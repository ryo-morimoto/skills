# Independent strategy briefs

`planning-modes.md` でmodeを確定し、P0を除き最低3候補を作る。
alternativesは同じ目的を**どう実現するか**、portfolioは根拠のある各領域を
**何からどう改善するか**を設計する。方式の対照だけが候補生成ではない。

## Choose real forks

- 現行module/state ownershipを保つか、責務を別境界へ移すか。
- 利用側に閉じるか、共通core・interfaceへ抽出するか。
- dependency inversionで外部を隔離するか、内部へ集約するか。
- 配布・互換条件の下で一括切替か、expand–migrate–contractか。

この一覧は候補軸で、固定三択ではない。実コードのcaller例と契約から選ぶ。
「小・中・大」だけ、別fileの修正、frontend担当とtest担当という工程分業は不可。
方針ごとの `direction / design_difference / weakness` を明記する。
見た目だけの代案や、根拠なく全面rewriteを追加しない。

## Common contract

全plannerに共通目的、成功シナリオ、scope、対象外、契約、予算・期間・尺度を渡す。
portfolioでは共通の全体scope内で担当領域の目的・scopeを区別する。
全候補を同じ対象の方式比較へ変換しない。工程分業ではなく各領域の完全な計画を求める。
比較条件は公開する。担当の方針・最適化目標だけを変え、他案の出力は見せない。
各案に最終構造、callerの使い方、移行DAG、中間状態、検証・回復、廃止条件、
残存負債、cost/risk/impact、根拠・未知を要求する。

方針を調べた結果「契約上不可能」「目的への便益がない」なら `infeasible` として
根拠を残す。三つの妥当案が残ることを強制しないが、最低三候補の実検討は省略しない。
不成立案と未提出を区別し、重複は水増ししない。条件内で候補が足りなければ不足を報告する。
hybridが必要なら新plan IDで再見積し、元案・追加scope・相互作用を残す。

## P0

P0は今回の改善投資をしない案。増分費用・削減は0だが、絶対維持負担・障害・
将来の期限は残る。既存リスクと、そのまま待てる条件を明記する。
P0が非交渉条件にfailしても基準として残し、実行可能な推薦にはしない。
