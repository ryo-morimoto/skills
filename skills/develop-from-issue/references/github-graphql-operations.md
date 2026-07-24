# GitHub Operations via `gh api graphql`

All issue and PR state changes in this workflow go through `gh api graphql`. Rules that apply to every recipe:

- Pass values as GraphQL variables (`-f` for strings, `-F` for typed values), never by interpolating user or issue content into the query string.
- Pass comment and issue bodies through files: `-f body="$(cat record.md)"` where `record.md` was written with a file tool.
- Read every write back before reporting it done. On an ambiguous error, query current state before retrying — never risk a duplicate write by retrying blindly.
- Node IDs (issue `id`, label `id`, PR `id`) come from a query first; numbers are for humans, IDs are for mutations.

Set once per session:

```bash
OWNER=<owner> REPO=<repo>
```

## One-time repository setup

Create the stage labels (skip any that already exist):

```bash
REPO_ID=$(gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) { id }
}' -f owner="$OWNER" -f repo="$REPO" --jq '.data.repository.id')

while read -r name color desc; do
  gh api graphql -f query='
  mutation($repoId: ID!, $name: String!, $color: String!, $desc: String) {
    createLabel(input: {repositoryId: $repoId, name: $name, color: $color, description: $desc}) {
      label { id name }
    }
  }' -f repoId="$REPO_ID" -f name="$name" -f color="$color" -f desc="$desc"
done <<'EOF'
stage:triage cccccc Awaiting routing through the upstream gate
stage:design 8250df Human-led requirement and design work
stage:ready 2da44e Decision recorded; implementable
stage:implementing 0969da Branch open; work in progress
stage:verify d4a72c PR open; awaiting verification verdict
stage:acceptance d93f0b Merged; awaiting validation by the requester
stage:tracking 6e7781 Split parent; sub-issues carry the work
EOF
```

If the deployment rejects `createLabel` as preview-only (older GitHub Enterprise Server), fall back once to `gh label create "<name>" --color <color> --description "<desc>"`; label *creation* is repository setup, not issue operation, so the REST fallback does not violate the GraphQL rule.

## Read issue state (phase 0)

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $number) {
      id
      title
      body
      state
      labels(first: 20) { nodes { id name } }
      comments(last: 50) { nodes { body createdAt author { login } url } }
      subIssues(first: 50) { nodes { number title state labels(first: 10) { nodes { name } } } }
      parent { number title }
    }
  }
}' -f owner="$OWNER" -f repo="$REPO" -F number="$ISSUE"
```

`subIssues` and `parent` are generally available since April 2025; on an older GitHub Enterprise Server without them, drop those fields and track children as a task list in the parent body.

Extract the current record of one type (latest marker wins):

```bash
... --jq '[.data.repository.issue.comments.nodes[]
          | select(.body | startswith("<!-- idd:triage -->"))] | last.body'
```

## Stage transitions

Resolve label IDs once per repository:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    labels(first: 20, query: "stage:") { nodes { id name } }
  }
}' -f owner="$OWNER" -f repo="$REPO"
```

Move between stages — remove the old label, add the new one (array variables use the `[]` syntax):

```bash
gh api graphql -f query='
mutation($id: ID!, $remove: [ID!]!, $add: [ID!]!) {
  removeLabelsFromLabelable(input: {labelableId: $id, labelIds: $remove}) { clientMutationId }
  addLabelsToLabelable(input: {labelableId: $id, labelIds: $add}) { clientMutationId }
}' -f id="$ISSUE_ID" -f 'remove[]='"$OLD_LABEL_ID" -f 'add[]='"$NEW_LABEL_ID"
```

First transition (no stage label yet) uses only the `addLabelsToLabelable` half. Read labels back after the mutation to confirm exactly one stage label remains.

## Post a record comment

Write the record to a file first, then:

```bash
gh api graphql -f query='
mutation($id: ID!, $body: String!) {
  addComment(input: {subjectId: $id, body: $body}) {
    commentEdge { node { url } }
  }
}' -f id="$ISSUE_ID" -f body="$(cat record.md)"
```

The returned `url` is the read-back verification; include it when reporting the state change.

## Split: create and attach sub-issues

```bash
CHILD_ID=$(gh api graphql -f query='
mutation($repoId: ID!, $title: String!, $body: String!, $labelIds: [ID!]) {
  createIssue(input: {repositoryId: $repoId, title: $title, body: $body, labelIds: $labelIds}) {
    issue { id number url }
  }
}' -f repoId="$REPO_ID" -f title="$TITLE" -f body="$(cat child-body.md)" \
   -f 'labelIds[]='"$TRIAGE_LABEL_ID" --jq '.data.createIssue.issue.id')

gh api graphql -f query='
mutation($parent: ID!, $child: ID!) {
  addSubIssue(input: {issueId: $parent, subIssueId: $child}) {
    issue { number }
    subIssue { number }
  }
}' -f parent="$PARENT_ID" -f child="$CHILD_ID"
```

Each child body must state observable behavior and done criteria (routing-gate.md); each child starts at `stage:triage`.

## Verify and integrate

PR ID from number:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) { id state mergeable reviewDecision }
  }
}' -f owner="$OWNER" -f repo="$REPO" -F number="$PR"
```

Merge on a pass verdict:

```bash
gh api graphql -f query='
mutation($id: ID!, $method: PullRequestMergeMethod!) {
  mergePullRequest(input: {pullRequestId: $id, mergeMethod: $method}) {
    pullRequest { merged mergedAt }
  }
}' -f id="$PR_ID" -f method=SQUASH
```

Use the repository's configured merge method; `SQUASH` is the default here because one issue slice maps to one commit on the default branch.

Discard on a decision-level failure (branch stays as evidence — do not delete it):

```bash
gh api graphql -f query='
mutation($id: ID!) {
  closePullRequest(input: {pullRequestId: $id}) {
    pullRequest { state closed }
  }
}' -f id="$PR_ID"
```

## Acceptance: close the issue

Only the acceptance gate closes issues — PRs reference issues with `Refs #N`, never closing keywords.

```bash
gh api graphql -f query='
mutation($id: ID!, $reason: IssueClosedStateReason!) {
  closeIssue(input: {issueId: $id, stateReason: $reason}) {
    issue { state stateReason }
  }
}' -f id="$ISSUE_ID" -f reason=COMPLETED
```

Use `NOT_PLANNED` when a cycle ends with the work abandoned rather than accepted.

## Find resumable work

List open issues at a given stage (quote the label because it contains `:`):

```bash
gh api graphql -f query='
query($q: String!) {
  search(query: $q, type: ISSUE, first: 20) {
    nodes {
      ... on Issue { number title url labels(first: 10) { nodes { name } } }
    }
  }
}' -f q="repo:$OWNER/$REPO is:issue is:open label:\"stage:verify\""
```
