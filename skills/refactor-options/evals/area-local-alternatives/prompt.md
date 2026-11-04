---
tags: [skill-creator]
max_turns: 70
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

領域別に改善したいですが、文字列ルールの重複を減らす領域については方式も最低3案比較したいです。
それとは別に、外部送信との結合を減らす候補を最低1案ください。P0は別枠です。
全体を3案に切り詰めず、同一領域の代替と領域間の組合せを区別してください。
公開signature、比較・戻り値・文字列・例外・sendの回数は保存してください。
単一runtime関数、データ表現の共有、生成時の同期などは探索のヒントであり、成立認定は不要です。
実績工数・変更頻度はありません。実装・tests実行・外部アクセスをせず、成立しない方式も正直に示してください。
読取りは入力とskill資源のみ、指示ベースです。保存は評価hostの指定先だけです。

Input files: labels.py, contract.md
