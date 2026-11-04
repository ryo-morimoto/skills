# Workflow and decision lifecycle

## States

`framing → grounded → alternatives → assessed → presented → selected / deferred / rejected`

- `needs_input`: 目的・scope・非交渉条件が決められない。
- `blocked`: 必須の並列context、権限、読取り、純粋計算が使えない。
- `stale`: 根拠snapshot、比較条件、選好、context revisionが変わった。
- `pending`: 資料を提示したが、人間がまだ選んでいない。

実装状態は存在しない。選択・資料保存・コード変更の承認は別物。

## Synchronization barriers

1. 全plannerへ渡す共通contextをfreezeする。
2. mode・領域mapを決め、最低3候補を新contextの同一parallel batchで起動する。
3. 全初回結果を回収するまで、他案を子へ渡さずcriticを始めない。
4. 新事実を確認したら共通revisionを上げ、影響する全案を更新する。
   無影響の再確認でも、誰がどの版で確認したかを残す。
5. 別contextのcriticが、同一版の全案を批評する。
6. 必要な修正を担当へ返す。通常一回。意味の違う新方針は別IDとする。
7. 型・算術・欠測を検査して表示し、人間へ戻す。

原案・不成立理由・評価者間の対立を消さない。親は候補の所有者ではなく比較の編集者。
criticの指摘を採らないなら理由を残す。`blocking` が残る案を無条件推薦しない。

## Failure and budget

planner失敗・timeoutは未完了であり、単一案で並列比較完了とは言わない。
再試行は一回まで、hostの予算内とする。成立候補が一つでも、複数方針を実際に
検討して他方針が不成立なら、P0と全候補・棄却理由を返せる。
候補生成自体が3未満なら完了にせず途中報告し、架空の案を追加しない。
費用不足で検討できない方針は「不成立」ではなく「未検討」と記す。

独立性は別contextという実行条件で、思考の無相関や正解を保証しない。
host traceなしの自己申告を「並列実行を検証済み」と表示しない。

## Decisions

`pending` にselected planや架空の回答を入れない。
`selected` には実際の回答、存在するplan ID、現在のcontext revisionが必要。
portfolioはplan_idsで複数／一部採用を表す。前提依存を閉じ、競合する組合せを避ける。
全領域を採ることや一つの勝者を強制せず、未採用・保留の領域を残す。
fail gateの案を選ぼうとしたら、矛盾を説明して変更・明示的条件見直しを確認する。
選好・目的の変更はcontext改訂として再比較し、前版の承認を持ち越さない。
選択を受けても「記録した。実装は開始していない」で終了する。
