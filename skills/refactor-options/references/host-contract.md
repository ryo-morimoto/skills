# Host capabilities and scope

独立したadapterは使わず、現在hostの実際のtoolを直接使う。
標準skill形式がsubagent・sandbox・model指定を提供するとは仮定しない。

## Capability checklist

- 独立した新contextのplannerを最低3つ、同じbatchで同時実行できる。
- 親の会話全体や他案を渡さず、共通contextと役割promptだけを渡せる。
- 結果を回収し、別contextのcriticを後から起動できる。
- 全子に許可read roots、secret除外、write禁止、外部送信禁止を伝えられる。
- bundled calculatorをstdin/stdoutで実行できる。
- role/context ID、call ID、batch、結果を実際のhost実行から記録できる。

並列呼出しをまとめる仕組みがあるhostでは、全plannerの起動を一つのparallel操作に
含める。foreground呼出しを一人ずつawaitして「並列」と呼ばない。
background実行なら全起動後の通知・joinで回収し、sleep/pollで代替しない。
hostが別tool名を使う場合も同じ契約を守る。特定model slugは固定しない。

## Permissions are not prompt text

read-onlyの強制が可能ならhostで設定する。`allowed-tools` だけでの保証は不可。
指示しか渡せないhostでは `instruction_only` と明示し、`enforced` と言わない。
利用者が強制隔離を要求した場合や、子がscopeを守る条件を確認できない場合はblocked。
tool実行の事実と、そのtoolが全不正操作を防ぐ保証は別物である。
本skillはhost設定・共有設定・global permissionを自動変更しない。

## OpenCode-style host

この環境のように新contextの `subagent` とparallel batchが使える場合、
plannerを同一batchで起動し、返却されたsession/context IDを記録する。
criticはplannerの完了後に新規起動する。子が親の同一会話を継ぐforkは使わない。
toolに読取り専用を強制する設定がないなら、全promptへ制約を渡したうえで
指示ベースの境界と報告する。対応確認を他hostへ一般化しない。

## Output and diagnostics

通常利用で `tests/`・`evals/`・package install・認証CLI・ネットワークを実行しない。
calculator自体はskillの固定資源であり、対象repoのコードをimportしない。
保存先の許可がない場合は返答とtool結果で引き継ぐ。
未取得のtimestamps、model IDs、tokens、料金は不明と記す。
packet中のrun_recordはtraceへの参照であって、そのJSONだけで実行を証明しない。

## What this package does not enforce

ネットワーク・filesystem権限をこのMarkdownやPythonがsandboxするわけではない。
実hostの強制隔離と、外部状態も含む監視評価はhost側の別責務。
並列実行が利用不可なら、文章だけの仮想planner比較へ縮退しない。
