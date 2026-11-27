# AREA: architecture questions

## 1. Purpose

At the Plan milestone, each member identifies at least one significant technical question to investigate. At the Final milestone, each member explains one architectural decision they materially contributed to: the need, the alternatives, the evidence, the decision, the trade-offs and the observed result.

The questions below are open: several answers are possible, and each one needs investigation before a decision. Each question is linked to the member's role and to the selected additional features.

| Member | Role | Question | Related features |
| --- | --- | --- | --- |
| PA | Workflow engine | How do we represent and execute a workflow? | ENG-TEMPLATES, ENG-ADR |
| Pierre | Authentication, services, infrastructure | How do we manage identities and delegated access? | SEC-GDPR, SYS-HEALTH |
| Tristan | Web client | What form should the builder take? | ENG-TEMPLATES (web), ENG-ADMIN |
| Florian | Mobile client, hooks | How does a hook detect an event exactly once? | SYS-SECRETS, SEC-DEPS |

## 2. PA: how do we represent and execute a workflow?

### Question

- How do we model nodes, links and the condition so that no maximum number of reactions is encoded in the data model?
- How do we check, when a workflow is saved, that every `{{ node.key }}` reference points to a key declared by an earlier node?
- How do we substitute values without ever evaluating user-supplied code?
- What happens at runtime when a referenced value is missing?

### Why it matters

The workflow engine is the core of the product. The subject requires structural validity to be checked when a workflow is saved, references outside the declared keys to be rejected, missing values to be handled deterministically, and substitution to replace data only. ENG-TEMPLATES reuses the same validation at import, and ENG-ADR requires a record about the workflow engine.

### Options to explore

- **Data model**: nodes and edges as relational rows, or the whole workflow as one JSON document.
- **Validation**: a graph walk that checks the structure (one trigger, at most one condition with two successors, no merging branches) and the scope of each reference.
- **Substitution**: a simple template parser that only resolves key paths, compared with a template engine (such as Jinja2) restricted to data access.
- **Missing values**: fail the run, skip the node, or substitute an empty value.

### How we will decide

- A POC that saves a workflow with a condition and 4 reactions, and rejects invalid structures and undeclared references.
- A test showing that a payload such as `{{ __import__('os') }}` is treated as plain text and never executed.
- An ADR documenting the chosen model and the missing value policy.

## 3. Pierre: how do we manage identities and delegated access?

### Question

- How do we link an external OIDC identity (for example Google) to a local account?
- What happens when the email of the external identity already belongs to a local account?
- How do we store OAuth2 tokens, refresh them before they expire, and revoke them when an account is deleted?

### Why it matters

The subject states that OIDC answers who the user is, while OAuth2 answers what the application may do on the user's behalf. It requires the identity linking and the lifecycle of delegated credentials to be documented as part of our data and security design. Hooks run without the user, so they depend on valid tokens. SEC-GDPR requires token revocation on account deletion, and SYS-HEALTH checks the identity providers.

### Options to explore

- **Identity linking**: automatic linking by verified email, explicit linking from an authenticated session, or one account per identity.
- **Token storage**: plain columns, application-level encryption, or a separate secrets store.
- **Token refresh**: refresh on demand before each call, or a scheduled task that refreshes tokens close to expiry.
- **Revocation**: call each provider's revocation endpoint, or only delete the tokens locally.

### How we will decide

- A POC with django-allauth: OIDC login, then a second login with the same email through another path.
- A POC of one service OAuth2 flow with storage, expiry, refresh and revocation.
- A table listing, for each selected service, its token lifetime and its revocation mechanism.

## 4. Tristan: what form should the builder take?

### Question

- Should the builder be a canvas with blocks and arrows, a list of steps, or a form-based wizard?
- Which form is the easiest to make accessible (WCAG AA, keyboard navigation, screen readers)?
- How do we help users choose the keys available from earlier nodes, without duplicating the server-side validation in the client?

### Why it matters

The subject leaves the form of the builder free but requires it to be justified. The builder is the most complex screen of the product and exists only on the web client. Both clients must meet WCAG AA, and the accessibility audit report must state what was measured and fixed.

### Options to explore

- **Canvas** (for example with React Flow): visual and flexible, but harder to use with a keyboard or a screen reader.
- **List of steps**: linear and accessible, well suited to our bounded model (a linear chain with at most one condition).
- **Form-based wizard**: guided and simple, but less convenient for editing an existing workflow.
- **Key selection**: a picker built from the node declarations exposed by the server catalogue, with the server remaining the only authority on validation.

### How we will decide

- Two quick prototypes (canvas and list of steps) of the same workflow.
- An axe or Lighthouse audit and a keyboard-only test on each prototype.
- A short comparison of the time needed to create a workflow with a condition and 4 reactions.

## 5. Florian: how does a hook detect an event exactly once?

### Question

- Should hooks poll the services at regular intervals, or receive webhooks when the service supports them?
- How do we identify an event that has already been processed: by identifier, by date, or with a cursor?
- What happens if the worker restarts or crashes in the middle of processing an event?

### Why it matters

The subject requires hooks to detect Actions and start workflows without any client open, and to avoid treating the same occurrence as a new event indefinitely. It explicitly states that how events are identified, scheduled and persisted is an architectural decision to document and defend. The mobile client displays what workflows did, so it depends on reliable hook results.

### Options to explore

- **Detection**: polling with Celery Beat, webhooks received by the server, or a mix depending on each service.
- **Deduplication**: a table of processed event identifiers with a unique constraint, or a cursor (last seen identifier or date) per hook.
- **Failure handling**: mark the event as processed in the same transaction as the creation of the execution, so a crash never leaves an event half processed.
- **Scheduling**: one task per workflow, or one task per service that checks all its workflows.

### How we will decide

- A POC of a polling hook that detects new items of a test service, then is restarted: no event is processed twice.
- A test where two workers try to process the same event at the same time: the unique constraint keeps only one.
- A table listing, for each selected service, whether it offers webhooks and what identifies an event.

## 6. Follow-up

Each member records the progress of their question in the Obsidian vault (`docs/notes/`). Once a question is decided, the decision becomes an ADR in `docs/adr/`, which is the evidence for the individual defense at the Final milestone.