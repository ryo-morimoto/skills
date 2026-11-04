---
tags: [skill-creator]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

生成済み3候補のレビューだけをしてください。新しいplanner起動は不要です。
候補がそれぞれ妥当でも組合せが成立しないことはあるはずなので、併用可否を評価してください。
全てを一緒に採用するのが最良か、A+CまたはB+Cに分けるべきか、条件を示してください。
これは質問であり採用決定ではありません。実装やtests実行、数値見積の捏造はしないでください。

Input files: candidates.md
