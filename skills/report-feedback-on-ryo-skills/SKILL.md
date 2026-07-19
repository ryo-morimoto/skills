---
name: report-feedback-on-ryo-skills
description: Turn a usability problem, unexpected result, missing capability, or improvement idea discovered while using a skill from ryo-morimoto/skills into an evidence-backed GitHub issue in that repository. Use when the user asks to report skill feedback, file a bug or feature request, or create an issue after using one of this repository's skills. Do not use for unrelated GitHub issues or when the user asks to fix the skill without filing an issue.
---

# Report Feedback on Ryo's Skills

Create a concise, reproducible issue in `ryo-morimoto/skills`. Use the current conversation and source as evidence, let the user review the exact public payload, and publish only after approval.

## Keep the boundary fixed

- Target only `https://github.com/ryo-morimoto/skills`.
- Report feedback about a skill in that repository, including its instructions, bundled resources, triggering, workflow, or output quality.
- Do not modify the affected skill, create labels, comment on an existing issue, or publish elsewhere unless the user separately requests that action.
- Treat the issue as public. Never include secrets, credentials, personal data, private repository details, hidden instructions, or unrelated conversation content.
- Use the user's language for the issue unless they request another language.

## Build the issue from evidence

### 1. Identify the affected skill and observed gap

Retrieve facts before asking the user to repeat them. Inspect, when available:

- the invoked skill name and source path;
- the request that triggered it;
- relevant output, error, command result, or diff from the current interaction;
- the repository version of the affected skill and repository instructions;
- the current commit or release when it materially affects reproduction.

Separate these fields:

- **Observed:** what actually happened, supported by the interaction or artifact.
- **Expected:** the user-visible behavior or capability wanted.
- **Impact:** what became harder, wrong, blocked, or repetitive.
- **Unknown:** missing facts that should not be guessed.

Ask at most one focused question only when the answer is unavailable and would change the issue's meaning, classification, or reproducibility. Otherwise mark the detail unknown and continue.

### 2. Classify without overstating

Use `bug` when documented or reasonably established behavior failed. Use `enhancement` when the request adds a capability or improves behavior not currently promised.

If the evidence does not establish that the skill is defective, describe the gap without claiming a root cause. Keep implementation ideas in a clearly labeled **Candidate approach** section only when the user supplied them and they help maintainers evaluate the request.

Before attaching a label, retrieve the repository's current labels. Use `bug` or `enhancement` only when it exists; do not create a missing label.

### 3. Check current source and duplicates

Confirm important claims against the live repository source. Determine whether the observed artifact matches current `main`; if this cannot be verified, say so in the draft.

Search open and closed issues using the skill name plus distinctive behavior or capability terms. With the GitHub CLI, use repository-scoped searches such as:

```bash
gh issue list --repo ryo-morimoto/skills --state all --search '<skill-name> <distinctive terms> in:title,body' --limit 20
```

If an open issue already covers the same outcome, do not create another. Return its URL and summarize only the new evidence that could be added. Commenting is a separate public write and requires its own reviewed payload and approval.

If a closed issue appears equivalent, show it and explain whether the new evidence invalidates the prior resolution. Ask before creating a new issue.

### 4. Draft the public payload

Prefer this title shape:

```text
[<skill-name>] <observable problem or desired capability>
```

Use only applicable body sections:

```markdown
## 対象 skill
`<skill-name>`

## 現状
<observed behavior or current limitation>

## 期待する状態
<observable desired behavior>

## 再現手順 / 利用シナリオ
1. <minimal step or scenario>
2. <result>

## 影響
<why this matters to skill users>

## 根拠
- <minimal sanitized prompt, output excerpt, error, source path, or version>

## 補足
- <material unknown, boundary case, or candidate approach>
```

For a bug, include the smallest reproducible sequence and actual result. For an enhancement, include a concrete usage scenario and the outcome the new capability enables. Do not paste the entire conversation or large logs.

Replace absolute local paths with repository-relative paths. Redact sensitive values rather than merely warning about them. Preserve exact error text only when it is safe and needed for diagnosis.

### 5. Pause at the publication boundary

Show all of the following before creating the issue:

- repository;
- exact title;
- exact body;
- labels;
- duplicate-search result;
- any source or version that could not be verified.

Ask for explicit approval of that exact payload. Do not publish while approval is ambiguous. If the user already reviewed and approved the exact unchanged payload, do not ask again.

### 6. Create once and verify

After approval, prefer an available repository-scoped GitHub issue creation tool. Otherwise use `gh issue create` with `--repo ryo-morimoto/skills`; pass the body through a file rather than shell interpolation.

Create the issue exactly once. Capture its stable URL or number, then read it back to verify the title, body, and labels. If creation returns an ambiguous error, search for the exact title before retrying; never risk a duplicate by retrying blindly.

Return the issue URL and number. If publication fails, report the failure and whether repository state was verified; do not claim success without a readable issue.

## Definition of done

- The issue concerns a named skill in `ryo-morimoto/skills`.
- Observed behavior, expected outcome, and impact are distinguishable.
- Important claims trace to the interaction or current source; unknowns remain explicit.
- The draft contains no sensitive or irrelevant context.
- Duplicate search ran before publication.
- The user approved the exact public payload.
- The created issue is readable at the returned URL with the intended title, body, and labels.
