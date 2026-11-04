# Evidence collection

許可scopeから、目的を説明する最小限の根拠を収集する。
全repoを網羅したと主張するより、実際に読んだ範囲と未調査を示す。

## Snapshot and boundaries

- revision、dirty状態、対象fileのpath・hash、読取り範囲を記録する。
- gitの情報を読む場合もfilesystem monitorや外部diffの起動に注意する。
  例: `git --no-optional-locks -c core.fsmonitor=false status --short`。
  diffが必要なら `--no-ext-diff --no-textconv` を使い、対象を限定する。
- secretや `.env*`、credential store、個人情報のdatasetを読まない。
  symlinkの実体を確認し、許可rootを越える参照は停止する。
- アプリのmodule import、package script、tests、formatter、DB/API呼出しで
  事実を確認しない。副作用のある追加調査は別途提案するだけにする。

## What to inspect

責務とstate ownership、主要なauthored callers、依存方向、公開API、戻り値・エラー、
副作用・権限・データ契約、配布単位、回復経路、既存testの内容、関連ADRを確認する。
generated/vendorの件数をauthored caller削減へ算入しない。
既存testの存在は合格や挙動同値性の証明ではない。

## Claims and IDs

- Evidence: ID、kind、source、何を支持するか、限界。
- Assumption: ID、出所のある仮定と、その条件。
- Unknown: ID、不足、どの判断が変わるか。

kindは `observed / analogous / expert / assumption / unknown`。
`expert` は人間・資料に出所がある見積に使い、LLMの自信を分類しない。
計算値は入力と式を示し、入力より強い証拠に昇格させない。
pathと行があるだけで真実とはせず、引用が主張を実際に支持するか読む。

新事実は親が確認して全案へ同じrevisionで配る。
plannerが自分だけ異なる契約・期間・チーム能力へ置き換えない。
コードや資料が途中で変わったら再確認するかstaleとする。
