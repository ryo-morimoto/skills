---
tags: [skill-creator]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

生成済みA/B/Cを独立criticとしてレビューしてください。新規planner起動は不要です。
各案の実質差と六観点の設計妥当性を分けて評価し、契約違反を便益や案数で相殺しないでください。
修正が必要なら元の案の問題を残して示し、勝手に直した案として合格にしないでください。
コードは静的に読むだけで、実装・tests実行・外部アクセスはしないでください。

Input files: source.py, candidates.md
