# AREA: selection of additional features

> Status: accepted for the Plan milestone (may be revised once, at the MVP milestone)
> Date: 2026-11-27
> Authors: PA, Pierre, Tristan, Florian

## 1. Summary

The group has 4 members, so the subject requires a total difficulty of at least **D >= 2 x 4 = 8**. We select **7 features for a total of 11 points**, across 3 domains (software engineering, security, systems).

| ID | Topic | Domain | Difficulty | Owner |
| --- | --- | --- | --- | --- |
| ENG-TEMPLATES | Shareable templates | Software engineering | 3 | PA (back-end) + Tristan (web) |
| SEC-GDPR | Personal data compliance | Security | 2 | Pierre |
| ENG-ADMIN | Administration area | Software engineering | 2 | Tristan |
| SEC-DEPS | Dependency scanning | Security | 1 | Florian |
| SYS-HEALTH | Health checks | Systems | 1 | Pierre |
| SYS-SECRETS | Secrets management | Systems | 1 | Florian |
| ENG-ADR | Architecture decision records | Software engineering | 1 | PA (all members contribute) |
| **Total** | | | **11** | |

Points per member: PA 2.5, Pierre 3, Tristan 3.5, Florian 2. Pierre also owns the infrastructure (Docker Compose stack and CI), which is not counted in these points.

## 2. Selection strategy

- **Safety margin**: 11 points instead of the minimum 8. A feature counts only when all its acceptance criteria can be observed, so the margin lets the largest feature (ENG-TEMPLATES, 3 points) fail without dropping below the threshold.
- **Several domains**: the selection covers software engineering, security and systems, as the subject recommends.
- **Consistency with our architecture**: SEC-GDPR, ENG-ADMIN, SYS-HEALTH and SEC-DEPS rely on our Django back-end, our Docker Compose stack and our CI. ENG-TEMPLATES relies on our workflow data model. ENG-ADR reuses our technology selection documents.
- **Real needs**: each feature answers a concrete user or operator need that we can demonstrate live.
- **Learning**: SEC-GDPR and ENG-TEMPLATES address topics nobody in the group has worked on yet (personal data lifecycle, portable and tamper-proof formats). ENG-ADMIN, SYS-HEALTH and SYS-SECRETS are lighter, but force us to look at the product from the operator's side.

AI features were not selected: the core product does not need a language model, and AI-NODE (3 points) is a prerequisite for most of them.

## 3. Feature details

### ENG-TEMPLATES: shareable templates (3 points)

**Customer need**: "I want to share an automation without sharing my credentials."

**Our reformulation**: a user can export an AREA as a file and send it to someone else, who imports it and connects it to their own accounts. No secret ever leaves the first user's account.

**Learning rationale**: designing a portable, versioned file format, guaranteeing its integrity, and making an import atomic (all or nothing).

**Planned implementation**:

- export endpoint producing a JSON file with the workflow structure (nodes, edges, parameters, key mapping), a `format_version` field, and no credential or token;
- integrity check with an HMAC signature computed by the server at export and verified at import;
- structural validation at import, reusing the validation applied when a workflow is saved;
- import inside a database transaction, so nothing is created when any check fails;
- web screens for export, import, and binding the template to the user's own service subscriptions.

**Acceptance criteria and where they will be observed**:

| Criterion | Where it is observed |
| --- | --- |
| A user exports an AREA from the web client as a single portable file containing no credentials or tokens | export button in the web client; the downloaded file is opened and inspected |
| Another user imports it and binds it to their own service subscriptions | second account in the web client, import screen |
| A missing service subscription is reported by name, and nothing is created | import with an account missing one service; error message and unchanged workflow list |
| A tampered or structurally invalid definition is rejected at import, and nothing is created | import of a file with one byte changed, then of a file with an invalid structure |
| The format is documented and versioned, including the policy for older versions | `docs/template-format.md` |

**Open questions**: which node parameters may contain personal or sensitive data (private channel IDs, email addresses), and whether they are exported, emptied or replaced by placeholders.

### SEC-GDPR: personal data compliance (2 points)

**Customer need**: "A user must be able to know what personal data we hold, export it and have it deleted without a developer."

**Our reformulation**: every personal data item is listed and justified, and the user can export it or delete their account themselves, with their third-party tokens revoked.

**Learning rationale**: mapping a personal data lifecycle from collection to deletion, and enforcing retention in code rather than only in documentation.

**Planned implementation**:

- data inventory document (`docs/data-inventory.md`);
- export endpoint and button in the web client, producing a JSON file (tokens excluded, since they are secrets);
- account deletion endpoint: calls each service's token revocation endpoint, then deletes the user's rows through Django cascade deletion, with a check of every table (including allauth tables and logs);
- scheduled Celery task that deletes execution records older than the documented retention period;
- security evidence sheet following the `area-security_evidence.pdf` template.

**Acceptance criteria and where they will be observed**:

| Criterion | Where it is observed |
| --- | --- |
| A committed data inventory maps personal data to purpose, storage location and retention | `docs/data-inventory.md` |
| An authenticated user exports their data from the web client in a machine-readable file | export button in the account settings of the web client |
| Account deletion leaves no personal data in the database beyond what is documented as deliberately kept | database queries after deletion, run during the demo |
| Account deletion revokes or destroys delegated third-party tokens | revocation calls in the server logs (sanitized), empty token table for the user |
| Retention of execution records is stated and technically enforced | retention task run on demand, old records removed |
| What deletion means for backups is documented | section in `docs/data-inventory.md` |

**Open questions**: retention period for execution records (for example 30 days), and what is deliberately kept after deletion (for example anonymized audit entries from ENG-ADMIN).

### ENG-ADMIN: administration area (2 points)

**Customer need**: "Support must administer the product without opening the database or stealing user credentials."

**Our reformulation**: support staff get a protected administration area where they can inspect and disable users and services, without ever seeing third-party tokens, and every action they take is recorded.

**Learning rationale**: role-based access control, and the difference between what an administrator needs to see and what they must not see.

**Planned implementation**:

- Django admin, restricted to `is_staff` accounts, served as an internal operations tool and not as a client of the product;
- `ModelAdmin` classes that explicitly exclude token fields;
- `enabled` flag on the service model, checked by the workflow engine and the hooks before triggering;
- disabled users refused on every login path (local, OIDC) and on already issued sessions or JWTs;
- audit through Django's `LogEntry`, extended to custom admin actions.

**Acceptance criteria and where they will be observed**:

| Criterion | Where it is observed |
| --- | --- |
| An administrator role protects an administration area, and a normal user is refused | `/admin` with a normal account, then with an admin account |
| Administrators can inspect and disable users and services: a disabled user can no longer authenticate, and AREA depending on a disabled service stop triggering | disable a user then try to log in; disable a service then check that its hooks stop |
| Administrators can inspect user AREA without learning third-party tokens | AREA and subscription pages in the admin area |
| State-changing administrative actions are audited with actor and time | admin action history |

The criterion about linking to execution records only applies when SYS-OBS is selected, which is not our case.

### SYS-HEALTH: health checks (1 point)

**Customer need**: "Tell me which dependency is failing."

**Our reformulation**: an operator can call one endpoint and immediately see which part of the product is down (database, hook worker, identity providers), without waiting and without learning any secret.

**Learning rationale**: dependency monitoring, and bounding checks so that the monitoring itself never hangs.

**Planned implementation**:

- `GET /health` endpoint in Django, returning JSON with one entry per dependency and a global status;
- checks: PostgreSQL (`SELECT 1`), Redis (`PING`), Celery worker (ping through the broker), OIDC provider (fetch of its discovery document);
- each check runs in parallel with a short timeout, so the endpoint answers within one second even when a dependency is unreachable;
- HTTP 200 when every required dependency is up, HTTP 503 when one is down;
- responses contain only names, statuses and durations: no connection string, secret or stack trace;
- the same endpoint is used by the Docker Compose healthcheck of the server container.

**Acceptance criteria and where they will be observed**:

| Criterion | Where it is observed |
| --- | --- |
| A machine-readable HTTP health endpoint reports each dependency separately: at least the database, the third-party authentication providers and whatever runs the hooks | `GET /health` response |
| A required dependency failure turns the answer into a failing status | HTTP 503 and `"status": "down"` on the failing entry |
| The evaluator stops the database container and sees it identified | live: `docker compose stop db`, then `GET /health` |
| Checks are bounded, so the endpoint answers within one second even when a dependency is unreachable | response time measured with `curl -w` while the database is stopped |
| No secret, connection string or stack trace is exposed | `GET /health` response with a failing dependency |

### SYS-SECRETS: secrets management (1 point)

**Customer need**: "Prove secrets do not leak through source, images or logs."

**Our reformulation**: no secret is ever committed, baked into an image or written to a log, and anyone can start the product from a documented example configuration.

**Learning rationale**: secret hygiene across the whole delivery chain (repository history, Docker images, runtime logs).

**Planned implementation**:

- gitleaks run as a pre-commit hook and in the CI, on the current content and the whole history, from the first day of development;
- complete `.env.example` with a description and a harmless placeholder for every variable;
- secrets passed to containers through environment variables in Docker Compose, never through committed files or image layers;
- logging configuration that filters `Authorization` headers and tokens, and `DEBUG` disabled outside development.

**Acceptance criteria and where they will be observed**:

| Criterion | Where it is observed |
| --- | --- |
| Secret scanning over current content and history is clean, or every historical secret is documented as revoked, with the proof | gitleaks report in the CI |
| A complete `.env.example` documents every required variable with a description and a harmless placeholder | `.env.example` at the repository root |
| A fresh clone configured from the example file starts a running product | live: clone, copy the example file, `docker compose up` |
| Secrets reach containers through the environment or an orchestrator secret mechanism | `docker-compose.yml` and Dockerfiles |
| No secret appears in any service log | live: `grep` over the logs of a full AREA run |

### SEC-DEPS: dependency scanning (1 point)

**Customer need**: "Show that vulnerable dependencies become visible and actionable."

**Our reformulation**: every contribution is scanned for known vulnerable dependencies on the server and both clients, and serious findings block the contribution.

**Learning rationale**: managing supply chain risk and deciding when a vulnerability can be accepted.

**Planned implementation**:

- dependency scan in the CI on every contribution: `pip-audit` for the server, `npm audit` (or an equivalent tool) for the web and mobile clients;
- contributions blocked from severity **high** upward (threshold to be confirmed);
- report stored as a CI artifact;
- accepted findings recorded in `docs/accepted-vulnerabilities.md` with their rationale and compensating measures;
- GitHub Dependabot alerts enabled so that newly disclosed vulnerabilities reach the team;
- security evidence sheet following the `area-security_evidence.pdf` template.

**Acceptance criteria and where they will be observed**:

| Criterion | Where it is observed |
| --- | --- |
| Dependency vulnerability scanning runs automatically on every contribution across the server and both clients | CI history |
| A stated severity threshold blocks contributions | CI history, or live with a known vulnerable dependency |
| The current report is reachable, and the group explains its most severe open finding | latest CI artifact |
| Accepted findings record rationale and compensating measures | `docs/accepted-vulnerabilities.md` |
| The group explains how a newly disclosed vulnerability reaches its attention | Dependabot alerts, explained during the defense |

### ENG-ADR: architecture decision records (1 point)

**Customer need**: "Leave the reasons behind important architecture choices, not a novel."

**Our reformulation**: every important architecture decision is recorded in a short, dated document, so that anyone taking over the project understands why it looks the way it does.

**Learning rationale**: arguing a decision against real alternatives, and keeping that reasoning alive when decisions change.

**Planned implementation**:

- records stored in `docs/adr/`, one file per decision, numbered and dated, with a status (proposed, accepted, superseded);
- first records derived from our technology selection documents (front-end, back-end, persistence);
- one record dedicated to the workflow engine (data model, validation, execution);
- the front-end record keeps the history of our change from React Native Web to React + React Native.

**Acceptance criteria and where they will be observed**:

| Criterion | Where it is observed |
| --- | --- |
| At least three significant ADRs, one about the workflow engine, each saying why it deserved a record | `docs/adr/` |
| Each gives context, real alternatives, decision and accepted consequences | content of each record |
| Rejected alternatives are rejected for this project, not declared universally bad | "Rejected options" section of each record |
| Records are dated and carry a status, and superseded decisions point to their replacement | header of each record |
| Any group member can describe the product under a rejected option chosen by the evaluator | oral, during the defense |

## 4. Milestones

| Milestone | Target |
| --- | --- |
| Plan | selection, rationale and owners documented (this document); ENG-ADR started with the technology selection documents |
| MVP | observable progress on at least a third of the points (at least 4 points): SYS-SECRETS and SEC-DEPS running in the CI, SYS-HEALTH endpoint served, ENG-ADMIN usable, first ADRs committed |
| MVP (optional) | last opportunity to revise this selection |
| Final | all acceptance criteria observable; security evidence sheets for SEC-GDPR and SEC-DEPS |

## 5. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| ENG-TEMPLATES is harder than estimated | 3 points lost | start the format and validation right after the workflow model is stable; split the work between back-end and web; report it to the local manager early if needed |
| Token revocation endpoints differ between services | SEC-GDPR incomplete | list each service's revocation mechanism while implementing its OAuth2 flow |
| A secret is committed by mistake | SYS-SECRETS requires proof of revocation | pre-commit hook from the first day; revocation procedure documented |
| A third-party identity provider is slow or down during the demo | SYS-HEALTH shows a failure unrelated to our product | mark identity providers as reported but not required in the global status if needed, and document the choice |
| Tristan carries ENG-ADMIN and the web part of ENG-TEMPLATES on top of the web client | workload imbalance | ENG-ADMIN relies mostly on Django admin; reassign it to Florian if the web client falls behind |