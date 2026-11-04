---
tags: [skill-creator]
max_turns: 50
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

税率追加の定義箇所を減らすため、同じ対象で最低3つのリファクタ方式を比較してください。
P0は別枠で、現状維持を三案の一つと数えないでください。
入力はこのケースのcheckout.py、invoice.py、contract.mdです。
公開signature、(total,tax)順、float/round、ValueError文言を保存してください。
期間12か月、実績工数と追加頻度はありません。第三案のためscopeを勝手に拡大しないでください。
各案の実質差と妥当性を評価し、重複なら正直に示してください。
計画のみで、実装やtests実行は不要です。指示ベースの読取り制約を認めます。

Input files: checkout.py, invoice.py, contract.md
