---
tags: [skill-creator]
max_turns: 50
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

この小さな注文処理の変更負担と外部依存との結合を減らしたいです。
価格ルール、永続化、通知の領域ごとに、具体的なリファクタ候補を最低3案出して比較してください。
P0は別枠です。同じ問題の方式三択にせず、各領域から少なくとも1候補を出してください。
併用・前提依存・作業や便益の重複も評価し、一案だけで全領域を解決する必要はありません。
現行の公開signature・tuple順・float/round・例外・SQL内容・通知文言と順序・回数を保存してください。
保存→通知の順序を変えず、失敗時に副作用を追加しないでください。
期間は12か月ですが実績工数・変更頻度はありません。不明は不明のまま残してください。
領域別の成功scenarioを示し、着手順や組合せは条件付きで判断したいです。
実装も既存testsの実行も不要です。指示ベースの読取り制約を認めます。

Input files: pricing.py, orders.py, contract.md
