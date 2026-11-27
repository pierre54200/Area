# Contributing

Thanks for contributing! This guide explains how we work together:
setup, branches, commits and pull requests.

## Table of contents

- [Setup](#setup)
- [Branches](#branches)
- [Commits](#commits)
- [Git hooks](#git-hooks)
- [Secrets](#secrets)
- [Pull requests](#pull-requests)

## Setup

Install [lefthook](https://lefthook.dev) and [gitleaks](https://github.com/gitleaks/gitleaks).
Both are required: without gitleaks, every commit is rejected.

On Ubuntu, install gitleaks from the official release:

```bash
# Get the latest release version number from GitHub
VERSION=$(curl -s https://api.github.com/repos/gitleaks/gitleaks/releases/latest | grep -Po '"tag_name": "v\K[^"]*')

# Download and extract the Linux binary
curl -sSfL "https://github.com/gitleaks/gitleaks/releases/download/v${VERSION}/gitleaks_${VERSION}_linux_x64.tar.gz" | tar -xz gitleaks

# Install it system-wide
sudo mv gitleaks /usr/local/bin/

# Check the installation
gitleaks version
```

On macOS: `brew install gitleaks`. On other systems, download the binary from the
[releases page](https://github.com/gitleaks/gitleaks/releases).

Then enable the Git hooks once, at the root of the repository:

```bash
lefthook install
```

The hooks check your commits and pushes automatically (see [Git hooks](#git-hooks)).

## Branches

| Branch | Role |
|---|---|
| `main` | Stable versions only. No direct commits. |
| `dev` | Integration branch. No direct commits. |
| `feat/...`, `fix/...`, ... | One branch per task, created from `dev`. |

Branch names follow `type/short-description`, in lowercase with dashes.
The type is the same as for commits.

```bash
git switch dev
git pull
git switch -c feat/main-menu
```

Examples: `feat/main-menu`, `fix/parser-crash`, `docs/install-guide`, `chore/update-gitignore`.

## Commits

Commits follow the [Conventional Commits](https://www.conventionalcommits.org) specification.
This format is **checked automatically** by a Git hook: a commit that does not follow it is rejected.

### Format

```
type(scope): description

optional body

optional footer
```

| Part | Required | Rules |
|---|---|---|
| `type` | yes | one of the types below, in lowercase |
| `(scope)` | no | the part of the project concerned, in lowercase: letters, digits, `.` `_` `-` `/` |
| `!` | no | right before `:`, marks a breaking change |
| `: ` | yes | a colon right after the type or scope, then one space |
| `description` | yes | a short summary of the change |
| body | no | details, after a blank line |
| footer | no | references to issues, after a blank line |

**The first line is 72 characters maximum.**

### Types

| Type | Use it for | Example |
|---|---|---|
| `feat` | a new feature | `feat(menu): add pause menu` |
| `fix` | a bug fix | `fix(parser): fix crash on empty file` |
| `docs` | documentation only (README, comments) | `docs: add build instructions` |
| `style` | formatting only, no code change | `style: fix indentation in player.cpp` |
| `refactor` | code change without behavior change | `refactor(network): split packet handling` |
| `perf` | performance improvement | `perf(render): cache textures` |
| `test` | adding or changing tests | `test(parser): add empty file test` |
| `build` | dependencies | `build: enable compiler warnings` |
| `ci` | GitHub Actions | `ci: add clang build` |
| `chore` | maintenance (.gitignore, hooks, config...) | `chore: ignore vgcore files` |
| `revert` | reverting a previous commit | `revert: remove pause menu` |

Not sure which type to use? Ask yourself: *does this change what the program does?*

- yes, it adds something: `feat`
- yes, it fixes something: `fix`
- no, it only reorganizes the code: `refactor`
- no, it only changes files around the code: `docs`, `build`, `ci`, `chore`, `test`

### Writing a good description

- Use the **imperative mood**, as if giving an order: "add", "fix", "remove", not "added" or "adds".
- Start with a **lowercase** letter.
- **No period** at the end.
- Say **what** the commit does, not how. The how is in the code.

A good test: the description should complete the sentence
*"If applied, this commit will..."*.

### Examples

Accepted:

```
feat: add main menu
fix(parser): fix crash on empty file
docs(readme): explain how to run the tests
build: add sanitizers in debug mode
refactor(network)!: change packet format
```

Rejected:

| Message | Why |
|---|---|
| `update` | no type |
| `Feat: add menu` | type in uppercase |
| `feat:add menu` | missing space after the colon |
| `fix : crash` | space before the colon |
| `update: player` | unknown type |
| `feat(Menu): add menu` | scope in uppercase |
| a first line over 72 characters | too long, move the details to the body |

### Body and footer

Use `git commit` without `-m` to open your editor and write a full message:

```
fix(parser): fix crash on empty file

The parser read the first line without checking that the file
had any content. It now returns a clear error instead.

Closes #12
```

- Leave a **blank line** after the first line.
- Explain **why** the change was needed, if it is not obvious.
- `Closes #12` closes issue 12 automatically when the commit reaches the default branch.

### Breaking changes

If a change breaks something that worked before (file format, command-line
options, public API), add `!` after the type or scope, and explain it in the footer:

```
refactor(config)!: rename the config file to settings.toml

BREAKING CHANGE: config.ini is no longer read. Rename your file.
```

### One commit, one change

- Keep commits **small and focused**: one logical change per commit.
- Do not mix a fix and a new feature in the same commit.
- Commit **code that compiles**.

### Automatic exceptions

Messages generated by Git itself are always accepted:
`Merge ...`, `Revert ...`, `fixup! ...`, `squash! ...`.

## Git hooks

| When | Check |
|---|---|
| commit | no direct commit on `main` or `master` |
| commit | no forbidden files: binaries, `*.o`, `vgcore.*`, `build/`... |
| commit | no leftover merge conflict markers (`<<<<<<<`, `>>>>>>>`) |
| commit | no secret (password, API key, token...) in the staged changes, checked by gitleaks |
| commit | the commit message follows the format above |
| push | the project compiles |

`git commit --no-verify` skips the hooks. **Do not use it**, except in a real emergency,
and tell the team. The secret scan also runs in the CI on the whole history,
so skipping the hook locally does not let a secret through.

## Secrets

Never commit a secret: passwords, API keys, OAuth client secrets, tokens,
private keys, Android keystores.

- Real values go in your local `.env` file, which is ignored by Git.
- `.env.example` lists every variable with a description and a harmless placeholder.
  When you add a variable, add it there too.
- If gitleaks blocks your commit, remove the secret from the file, use an
  environment variable instead, and stage the file again.
- If gitleaks reports a false positive, ask the team before adding an exception
  to `.gitleaks.toml`. Every exception must be justified.

To scan the whole repository and its history by hand:

```bash
gitleaks git --redact --verbose .
```

### If a secret was pushed

Removing the commit is **not enough**: the secret may already have been copied.

1. **Revoke it immediately** with the service that issued it (regenerate the key, change the password).
2. Replace it with an environment variable.
3. Tell the team, and record the revocation (date, service, proof) in the documentation.

## Pull requests

- One pull request = one topic. Keep it small (ideally under 400 changed lines).
- Target `dev`. Only `dev` is merged into `main`.
- The **title follows the same format as commits**: `feat(menu): add main menu`.
  It is checked automatically, and it becomes the commit message after a squash merge.
- Fill in the template, and link the issue with `Closes #12`.
- Open it as a **Draft** while it is not finished.

Before merging:

- at least **one review** from another team member;
- all review comments are resolved;
- the CI is green.

Merging:

- `feat/...`, `fix/...` into `dev`: **Squash and merge**;
- `dev` into `main`: **Create a merge commit**;
- delete the branch after merging.