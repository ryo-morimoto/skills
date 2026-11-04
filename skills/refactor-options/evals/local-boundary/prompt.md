---
tags: [skill-creator]
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

税率を追加する際の変更箇所を減らすリファクタ計画を比較してください。
対象は入力の checkout.py / invoice.py のみです。現状維持案も残してください。
外部関数のsignature、返すtupleの順、丸め、エラー文言は変えないでください。
比較期間は12か月です。実績工数・変更頻度・削減量の履歴はありません。
推定する場合は仮定と分かるようにし、不明な値を0で埋めないでください。
最終的な構造だけでなく、移行途中・検証・回復も比較したいです。
実装や既存testsの実行は不要です。コードは変更しないでください。
この評価では読取りscopeをfixtureとskill資源に限定する指示ベースの制約を認めます。
強制sandboxがあると偽らず、並列plannerやcriticを起動した場合は実際のtool IDを残してください。

Input files: checkout.py, invoice.py, contract.md
