---
tags: [skill-creator]
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

この小さな出荷処理について、変更負担を減らすリファクタ候補を洗い出してください。
領域の分け方からコードを根拠に考え、最低3つの変更候補とP0を比較したいです。
特定の三領域や、同じ問題の方式三択には固定しません。着手順・併用条件も示してください。
公開関数、返す文字列、例外、副作用の順序と回数は保存してください。
期間12か月、工数・変更頻度の実績はありません。実装・tests実行・外部アクセスは不要です。
読取りは入力とskill資源のみ、制約は指示ベースです。保存は評価hostが指定した出力先だけです。

Input files: dispatch.py, contract.md
