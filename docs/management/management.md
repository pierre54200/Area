# AREA: project management method and tools

## 1. Summary

We work with a **Kanban flow organised around the 3 project milestones** (Plan, MVP, Final), tracked in a single **GitHub Project**. Work items are **GitHub issues** created from custom templates (bug, feature). Quality rules are enforced locally by **Lefthook** git hooks and remotely by the CI and branch protection. Team knowledge (research, meeting notes, decisions in progress) lives in an **Obsidian** vault.

| Need | Tool |
| --- | --- |
| Planning and task tracking | GitHub Project (board + roadmap views) |
| Milestones | GitHub milestones: Plan, MVP, Final |
| Work items | GitHub issues with custom templates (bug report, feature request) |
| Local quality checks | Lefthook (commit message, build, conflict markers, branch) |
| Remote quality checks | GitHub Actions (lint, tests, build) + GitHub rulesets protecting `main` and `dev` and enforcing branch names |

## 2. Method

### Options considered

| Method | Principle | Fit for our project |
| --- | --- | --- |
| Scrum | fixed sprints (1 or 2 weeks), sprint planning, daily stand-up, review and retrospective, roles (product owner, scrum master) | rituals and roles are heavy for 4 students over a few weeks; the milestones already give us a fixed rhythm |
| Kanban | continuous flow on a board, limit on work in progress, no fixed sprint | light, visual, adapts to unequal workloads between members; needs discipline to avoid tasks piling up |
| Waterfall | sequential phases (design, build, test) | contradicts the subject, which expects plans to change based on evidence |

### Decision

**Kanban, organised by milestones**, because:

- the 3 milestones already split the project into fixed periods with clear deliverables, so Scrum sprints would add rituals without adding structure;
- members work on different layers (server, web, mobile, infrastructure) at different paces, which a continuous flow handles better than a shared sprint commitment;
- the board makes blocked tasks and overloaded members visible at a glance.

Rejected for this project: Scrum (too many rituals and roles for our size and duration), Waterfall (no room for the plan revisions the subject expects at the MVP milestone).

### Rules of the flow

- **Board columns**: Backlog, To do, In progress, In review, Done.
- **Work-in-progress limit**: at most 2 issues "In progress" per member, so tasks are finished before new ones are started.
- **Weekly sync** (about 30 minutes): review the board, move priorities, identify blocked tasks and rebalance work.
- **Milestone review**: before each defense, compare the plan with what actually happened and write down the meaningful changes, their reason and their cost (required at the MVP milestone).

## 3. GitHub Project

One GitHub Project holds every task of the whole project.

### Milestones

| Milestone | Content |
| --- | --- |
| Plan | technology selection documents and POCs, selection of additional features, architecture questions, task breakdown, this document |
| MVP | deployable product, end-to-end workflow with a trigger, at least two reactions and one condition, first technical documentation, CI, progress on at least a third of the feature points |
| Final | complete product, all selected features, documentation, accessibility audit, post-mortem, presentation |

### Issue fields

Each issue carries the information the subject requires for a task breakdown (actionable, scheduled, assigned, dependencies identified):

| Field | Purpose |
| --- | --- |
| Assignee | the member responsible |
| Milestone | Plan, MVP or Final |
| Start date and target date | custom project fields, used by the roadmap view |
| Area | custom field: server, web, mobile, infra, docs |
| Feature | custom field linking the issue to a selected additional feature (ENG-TEMPLATES, SEC-GDPR, etc.), or "core" |
| Dependencies | "Blocked by" list in the issue body (for example `Blocked by #12`) |

### Views

- **Board**: the Kanban flow, grouped by status.
- **Roadmap**: issues on a timeline using start and target dates, grouped by milestone.
- **By member**: issues grouped by assignee, to check that the workload is balanced.

### Issue templates

Custom templates live in `.github/ISSUE_TEMPLATE/` as GitHub issue forms, so every issue is created with the same structure.

**Bug report** (`bug_report.yml`):

- description of the problem;
- steps to reproduce;
- expected and actual behaviour;
- affected area (server, web, mobile, infra);
- environment (browser, Android version, commit);
- label `bug` added automatically.

**Feature request** (`feature_request.yml`):

- user need (who wants what, and why);
- acceptance criteria, written so they can be observed;
- affected area;
- related additional feature, if any;
- dependencies (`Blocked by #...`);
- label `feature` added automatically.

## 4. Git workflow

### Branches

| Branch | Role | Merged from |
| --- | --- | --- |
| `main` | stable version, delivered at each milestone | `dev`, through a pull request |
| `dev` | integration branch, where finished work is gathered | work branches, through pull requests |
| `<type>/<issue-number>-<short-description>` | one branch per issue, created from `dev` | |

Examples of work branches: `feat/42-workflow-validation`, `fix/57-oauth-refresh`, `docs/12-tech-choice-backend`.

### GitHub rulesets

Repository rulesets enforce the workflow on the GitHub side, so the rules apply even when a local hook is skipped:

- **`main` and `dev` are protected**: no direct push, no force push, no deletion; every change goes through a pull request;
- **the CI must pass** (lint, tests, build) before a pull request can be merged;
- **at least one approval** from another member is required;
- **branch names must follow the convention** `<type>/<issue-number>-<short-description>`, where `<type>` is one of `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`.

### Pull requests and commits

- Pull requests reference their issue (`Closes #42`) so the board updates automatically.
- At least one other member reviews each pull request before it is merged.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/): `feat(server): validate workflow references`, `fix(mobile): keep server address after restart`.

## 5. Lefthook

Lefthook runs git hooks defined in a single `lefthook.yml` file at the repository root. Every member installs it once with `lefthook install`.

| Hook | Check | Why |
| --- | --- | --- |
| `commit-msg` | the message follows Conventional Commits | readable history, changelog generation later |
| `pre-commit` | no merge conflict markers left in staged files | avoid committing a half-resolved merge |
| `pre-commit` | the changed part of the code compiles and passes the linter (server, web, mobile) | broken code never reaches a commit |
| `pre-push` | the branch is not `main` or `dev` and follows the naming convention | changes always go through a pull request on the right branch |

Example configuration (paths assume a monorepo with `server/`, `web/` and `mobile/` folders, to be adapted):

```yaml
commit-msg:
  commands:
    conventional-commit:
      run: |
        # Reject commit messages that do not follow Conventional Commits
        head -n1 {1} | grep -Eq '^(feat|fix|docs|style|refactor|test|chore|ci|build|perf)(\([a-z0-9-]+\))?!?: .+' \
          || { echo "Commit message must follow Conventional Commits, e.g. 'feat(server): add hook scheduler'"; exit 1; }

pre-commit:
  parallel: true
  commands:
    conflict-markers:
      run: |
        # Block commits that still contain merge conflict markers
        if grep -nE '^(<<<<<<<|>>>>>>>)( |$)' {staged_files}; then
          echo "Merge conflict markers found"; exit 1
        fi
    server-check:
      glob: "server/**/*.py"
      run: cd server && ruff check . && python -m compileall -q .
    web-check:
      glob: "web/**/*.{ts,tsx}"
      run: cd web && npx eslint . && npx tsc --noEmit
    mobile-check:
      glob: "mobile/**/*.{ts,tsx}"
      run: cd mobile && npx eslint . && npx tsc --noEmit

pre-push:
  commands:
    branch-check:
      run: |
        # Forbid direct pushes to protected branches and enforce the branch naming convention
        branch=$(git rev-parse --abbrev-ref HEAD)
        if [ "$branch" = "main" ] || [ "$branch" = "dev" ]; then
          echo "Direct push to $branch is forbidden, open a pull request"; exit 1
        fi
        echo "$branch" | grep -Eq '^(feat|fix|docs|refactor|test|chore|ci)/[0-9]+-[a-z0-9-]+$' \
          || { echo "Branch name must look like 'feat/42-short-description'"; exit 1; }
```

**Limit**: local hooks can be skipped with `--no-verify`. They are a fast feedback for members, not a guarantee. The guarantee comes from the CI and the GitHub rulesets on `main` and `dev`, which run the same checks on every pull request and make a failure visible on it, as the subject requires for the MVP.