# AREA: persistence technology selection

## 1. Context and needs

The database stores data of very different kinds:

- **user accounts**: local identity, linked external identities (OIDC), account confirmation;
- **service subscriptions** and **delegated OAuth2 tokens** (access and refresh tokens), the most sensitive data in the system;
- **workflows**: one trigger node, reaction nodes, at most one condition with two branches, each node's parameters and the key mapping (`{{ trigger.subject }}`). The structure varies with the node type;
- **hook state**: last processed event, cursor or seen identifiers, so the same occurrence is never processed twice;
- **execution history**: each run, its nodes, their inputs and outputs, and the outcome.

Constraints:

- the HTTP server and the hook worker access it **at the same time**;
- several operations must be **atomic**, for example marking an event as processed and creating the matching execution;
- the database must run in **Docker Compose** and be well supported by **Django**, our back-end choice.

## 2. Evaluation criteria

| Criterion | Weight | What we measure |
| --- | --- | --- |
| Security | 3 | role-based access control, encrypted connections (TLS), column encryption options, vulnerability history, backups |
| Integrity and transactions | 3 | ACID transactions, unique constraints and foreign keys (useful for event deduplication) |
| Semi-structured data | 2 | storing and querying node parameters with a variable format |
| Concurrency | 2 | simultaneous access from the server and the worker |
| Django integration | 2 | support by the ORM and migrations |
| Team skills | 2 | ramp-up time for the 4 members |
| Operations in Docker | 1 | official image, simple backup and restore |

## 3. Options considered

**Option A: PostgreSQL.** A full relational database: ACID transactions, constraints, roles. The **JSONB** type stores indexable JSON documents, handy for variable node parameters while keeping relational tables for everything else. The engine best supported by Django (specific fields in `django.contrib.postgres`). Standard backup tools (`pg_dump`, `pg_restore`).

**Option B: MySQL / MariaDB.** Relational, very widespread, well supported by Django. A JSON type exists, but querying and indexing that data is less rich than with JSONB.

**Option C: MongoDB.** A document database: a whole workflow can fit in a single document. Trade-offs: Django's ORM does not officially support it, relations (user, subscriptions, tokens, executions) are less natural, and referential integrity must be handled in code.

**Option D: SQLite.** A database in a single file, ideal for tests and POCs. Trade-offs: only one writer at a time, which is a problem with a server and a worker writing in parallel. No user or role management.

## 4. Comparison

Scores from 1 (poor) to 5 (excellent). For team skills, 0 means nobody in the team knows the technology. **Provisional scores, to be confirmed or corrected with the POC results.**

| Criterion (weight) | A: PostgreSQL | B: MySQL/MariaDB | C: MongoDB | D: SQLite |
| --- | --- | --- | --- | --- |
| Security (3) | 5 | 4 | 4 | 2 |
| Integrity and transactions (3) | 5 | 5 | 3 | 4 |
| Semi-structured data (2) | 5 | 3 | 5 | 2 |
| Concurrency (2) | 5 | 4 | 4 | 1 |
| Django integration (2) | 5 | 4 | 1 | 5 |
| Team skills (2) | 2 | 0 | 0 | to score |
| Operations in Docker (1) | 5 | 5 | 5 | 4 |
| **Weighted total** | **69** | **54** | **46** | **38 (excluding skills)** |

Rationale for the main scores:

- **Security**: PostgreSQL offers fine-grained roles, TLS and extensions such as pgcrypto. In every case, OAuth2 tokens will be encrypted by the application before being stored (see SEC-CRYPTO if that feature is selected). The database then only sees ciphertext.
- **Integrity**: a unique constraint on (hook, event identifier) directly prevents an event from being processed twice, even with two workers running.
- **Team skills**: the team has some experience with PostgreSQL and none with MySQL or MongoDB.
- **MongoDB**: a very good fit for workflows, but the lack of official support in the Django ORM rules it out for this project. It is not a bad choice in general.

## 5. Data model sketch

Hybrid model: relational tables for entities and their links, JSONB for what depends on the node type.

| Table | Role | Main fields |
| --- | --- | --- |
| `user` | local account | id, email, hashed password, language, confirmed, created at |
| `external_identity` | OIDC identity linked to an account | id, user_id, provider, subject (unique per provider) |
| `service_subscription` | a user's subscription to a service | id, user_id, service, encrypted access_token, encrypted refresh_token, expiry, scopes |
| `workflow` | a workflow or an AREA | id, user_id, name, enabled, version, created at, updated at |
| `workflow_node` | a workflow node | id, workflow_id, type (trigger, reaction, condition), service, action or reaction, `params` (JSONB), position |
| `workflow_edge` | link between two nodes | id, workflow_id, source_id, target_id, branch (null, true, false) |
| `hook_state` | hook state for a workflow | id, workflow_id, cursor (JSONB), last check |
| `processed_event` | events already processed | id, workflow_id, event_id, processed at; unique constraint (workflow_id, event_id) |
| `execution` | a workflow run | id, workflow_id, triggered at, finished at, status |
| `execution_step` | an executed node | id, execution_id, node_id, inputs (JSONB), outputs (JSONB), status, error |

Design notes:

- nodes and their links are rows, not a fixed-size array. The model therefore sets **no maximum** on the number of reactions, as the subject requires;
- structural rules (at most one condition, two successors for a condition, branches that do not merge) are checked by the server when the workflow is saved;
- tokens are never stored in clear text.

## 6. Practical evidence (POCs)

Each POC must be committed to the repository under `poc/persistence/<option>/`, with a short README of the results.

| POC | Goal | Result |
| --- | --- | --- |
| A1 | Django models `workflow`, `workflow_node`, `workflow_edge` on PostgreSQL, with a workflow containing 4 reactions and one condition | to be completed |
| A2 | query on a JSONB field of the node parameters | to be completed |
| A3 | two workers insert the same event: the unique constraint keeps only one | to be completed |
| A4 | `pg_dump` backup, then restore into a fresh container | to be completed |
| C1 | same workflow stored as a MongoDB document, comparison of reading and validation | to be completed |
| D1 | concurrent write test on SQLite (server + worker) | to be completed |

## 7. Decision

**Provisional choice: PostgreSQL, with a hybrid relational + JSONB model.**

Reasons:

- transactions and unique constraints, which guarantee that an event is processed only once;
- JSONB for variable node parameters, without giving up relations;
- the best support in Django, and simple backup and restore in Docker.

Accepted consequences:

- part of the validation of JSONB parameters happens in code, not in the schema;
- some `django.contrib.postgres` features tie us to PostgreSQL. Switching engines would require adaptation;
- SQLite may still be used for some fast tests, but integration tests run on PostgreSQL.

This decision will be reviewed after the POCs, and any change will be documented with its reason and consequences.