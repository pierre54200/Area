# AREA: back-end technology selection

## 1. Context and needs

The application server holds all the business logic. Both clients only handle presentation. The server must:

- expose an **HTTP API described with OpenAPI**, with a browsable interface. This description is the contract between members, and a test must fail when it does not match the implementation;
- handle **local authentication** (registration, account confirmation, login) and **OIDC authentication** through an external provider;
- handle **delegated OAuth2 access** to third-party services, and store and refresh tokens for hooks that run without the user;
- expose the **catalogue** of services, Actions and REActions (`about.json`) without a hard-coded list on the client side;
- **validate workflows when they are saved**: structure (at most one condition, two branches) and `{{ node.key }}` references limited to declared keys;
- **execute workflows**: data substitution that never evaluates user code, and deterministic behaviour when a value is missing;
- run **hooks autonomously**, with no client open, without processing the same event over and over;
- build and run with **Docker Compose**.

## 2. Evaluation criteria

Each option gets a score from 1 to 5 per criterion, then the total is weighted. The group should adjust the weights.

| Criterion | Weight | What we measure |
| --- | --- | --- |
| Security | 3 | password hashing, CSRF, SQL injection protection, session/JWT handling, vulnerability tracking, maturity of OIDC/OAuth2 libraries |
| OpenAPI | 3 | description generated from code, Swagger interface, ease of testing conformance |
| OIDC and OAuth2 auth | 2 | ready-made libraries for OIDC and many OAuth2 providers |
| Background jobs | 2 | solutions to run hooks and schedule tasks |
| Productivity | 2 | ORM, migrations, validation, admin, amount of code to write |
| Team skills | 2 | ramp-up time for the 4 members |
| Testing | 1 | unit and functional testing tools |
| Ecosystem and maturity | 1 | documentation, community, maintenance |

## 3. Options considered

**Option A: Django + Django REST Framework (Python).** A full framework: ORM, migrations, authentication, default security protections. DRF adds API serialization and validation. drf-spectacular generates the OpenAPI 3 description and a Swagger interface. django-allauth covers OIDC and many OAuth2 providers. Trade-offs: Django is mostly synchronous, and background jobs need a separate tool (Celery or similar). Django must be used as an API only, without its templates, to keep the client/server separation.

**Option B: NestJS (TypeScript).** Modular architecture inspired by Angular, with dependency injection. The `@nestjs/swagger` module generates OpenAPI from decorators. Same language as the clients, so types can be shared. Trade-offs: more building blocks to choose and assemble (an ORM such as Prisma or TypeORM, Passport for auth, BullMQ for jobs).

**Option C: Spring Boot (Java/Kotlin).** Very robust, Spring Security is a reference for OIDC and OAuth2, and springdoc generates OpenAPI. Trade-offs: verbose, heavy configuration, slow startup, and a steep learning curve for a project lasting a few weeks.

## 4. Comparison

Scores from 1 (poor) to 5 (excellent). For team skills, 0 means nobody in the team knows the technology. **Provisional scores, to be confirmed or corrected with the POC results.**

| Criterion (weight) | A: Django + DRF | B: NestJS | C: Spring Boot |
| --- | --- | --- | --- |
| Security (3) | 5 | 4 | 5 |
| OpenAPI (3) | 4 | 4 | 4 |
| OIDC and OAuth2 auth (2) | 5 | 4 | 5 |
| Background jobs (2) | 4 | 5 | 4 |
| Productivity (2) | 5 | 4 | 3 |
| Team skills (2) | 3 | 3 | 0 |
| Testing (1) | 4 | 4 | 5 |
| Ecosystem (1) | 5 | 4 | 5 |
| **Weighted total** | **70** | **64** | **61** |

Rationale for the main scores:

- **Security**: Django hashes passwords by default (PBKDF2, with Argon2 available), protects against CSRF and uses a parameterized ORM. Spring Security offers a comparable level, at the cost of more configuration.
- **OpenAPI**: all three rely on a mature library (drf-spectacular, `@nestjs/swagger`, springdoc).
- **Background jobs**: NestJS integrates directly with BullMQ. Django works very well with Celery + Redis, but it adds one more component to deploy.
- **Team skills**: nobody in the team knows Spring Boot, which offsets its strengths in security and authentication.

## 5. Running hooks in the background

Hooks must run with no client open and without processing the same event twice. This requires a process separate from the HTTP server. Options for Django:

| Option | Principle | Pros | Cons |
| --- | --- | --- | --- |
| Celery + Redis + Celery Beat | message broker, workers, scheduler | standard, robust, scalable, paves the way for ENG-ASYNC | two more containers (Redis, worker), more configuration |
| Looping Django command | a `manage.py run_hooks` command in its own container | very simple, no external component | scheduling and error recovery must be written by hand |
| django-q2 or Huey | lighter task queue, can use the database as broker | fewer components than Celery | smaller ecosystem |

Provisional choice: **Celery + Redis**, because it cleanly separates workflow execution from the HTTP server. Event deduplication (an identifier or cursor persisted per hook) is stored in the database, independently of the broker.

## 6. Practical evidence (POCs)

Each POC must be committed to the repository under `poc/backend/<option>/`, with a short README of the results.

| POC | Goal | Result |
| --- | --- | --- |
| A1 | Django + DRF API with registration, login, and an OpenAPI description served by drf-spectacular | to be completed |
| A2 | OIDC login (Google for example) with django-allauth | to be completed |
| A3 | hook scheduled by Celery Beat that detects an event without processing it twice | to be completed |
| A4 | test that fails when the implementation and the OpenAPI description diverge (for example with schemathesis) | to be completed |
| B1 | same endpoints as A1 in NestJS with `@nestjs/swagger` | to be completed |
| C1 | same endpoints as A1 in Spring Boot with springdoc | to be completed |

Questions the POCs must answer:

1. How much code does a complete OpenAPI description take, error responses included?
2. Do the OIDC flow and a service OAuth2 flow work easily with the chosen library?
3. Does the hook run with no client and no duplicates after a restart?

## 7. Decision

**Provisional choice: Django + Django REST Framework, with drf-spectacular for OpenAPI, django-allauth for OIDC and OAuth2, and Celery + Redis for hooks.**

Reasons:

- default security protections and mature authentication libraries;
- built-in ORM and migrations, which speed up persistence work;
- OpenAPI generation with a Swagger interface, which directly meets the subject requirement.

Accepted consequences:

- two languages in the project: Python for the server, TypeScript for the clients. Client-side types are generated from the OpenAPI description, which makes up for the lack of direct sharing;
- Redis and a Celery worker added to Docker Compose;
- Django used as an API only, without its HTML templates.

This decision will be reviewed after the POCs, and any change will be documented with its reason and consequences.