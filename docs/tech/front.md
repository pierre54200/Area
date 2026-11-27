# AREA: front-end technology selection

## 1. Context and needs

We must deliver two clients that consume the same server HTTP API, described with OpenAPI. The decision is about the **web framework + mobile framework pair**, because it drives code sharing and how the work is split between the 4 members.

Subject requirements that weigh on this choice:

- **Web client**: works on common browsers, and is the only client that contains the workflow builder (nodes and data mapping).
- **Mobile client**: Android is mandatory, with a configurable server address. It lists, enables, disables and monitors workflows. iOS is a bonus.
- **Accessibility**: WCAG AA on both clients, with a committed audit report.
- **i18n**: at least two languages across the whole main flow, from registration to the creation of an AREA.
- **Reproducible build**: the Android APK must be produced by Docker Compose.
- **Client/server separation**: full-stack frameworks are discouraged, and business logic stays on the server.
- **Authentication**: local login, OIDC and service OAuth2, including on mobile (redirects and token storage).

## 2. Evaluation criteria

Each option gets a score from 1 to 5 per criterion, then the total is weighted. Weights reflect the subject requirements and the team size. The group should adjust them.

| Criterion | Weight | What we measure |
| --- | --- | --- |
| Security | 3 | default XSS protection, secure token storage on mobile, OAuth2 with PKCE on mobile, dependency vulnerability tracking |
| Accessibility | 3 | how easily WCAG AA can be reached (semantics, focus, keyboard, screen readers), available audit tools |
| Web/mobile code sharing | 3 | amount of shared code: i18n, API client, types, validation, components |
| Builder fit | 2 | libraries available for a node editor or a step list |
| Team skills | 2 | ramp-up time for the 4 members |
| i18n | 1 | mature library, plurals, date formats |
| Android build in Docker | 1 | APK produced without manual steps |
| Ecosystem and maturity | 1 | documentation, community, active maintenance |
| iOS bonus | 1 | ability to target iOS without a rewrite |

## 3. Options considered

**Option A: React (web) + React Native (mobile).** Two applications, same language and same concepts. The web client gets the whole React DOM ecosystem (React Flow for the builder, semantic HTML for accessibility). Sharing is still possible through a common package: types, API client generated from the OpenAPI description, translation files. Screens are written twice.

**Option B: React Native Web + React Native (Expo).** A single TypeScript codebase compiles to web, Android and iOS. Platform-specific screens use `.web.tsx` / `.native.tsx` files, which lets us keep the builder web-only. Risks: web rendering goes through an abstraction layer, web accessibility is less fine-grained than hand-written HTML, and DOM libraries such as React Flow can only be used in web-specific files.

**Option C: Angular (web) + Ionic/Capacitor (mobile).** A very structured web framework with built-in routing, forms, HTTP client and i18n, and default XSS/XSRF protections. Ionic reuses Angular for mobile and Capacitor packages it as an APK. Trade-offs: steeper learning curve (RxJS, dependency injection), and the mobile app renders inside a WebView.

**Option D: React (web) + Flutter (mobile).** Flutter gives very good Android rendering and iOS support. But it means two languages (TypeScript and Dart) and two ecosystems: no code shared between the clients, and i18n is done twice.

## 4. Comparison

Scores from 1 (poor) to 5 (excellent). For team skills, 0 means nobody in the team knows the technology. **Provisional scores, to be confirmed or corrected with the POC results.**

| Criterion (weight) | A: React + RN | B: RN Web + RN | C: Angular + Ionic | D: React + Flutter |
| --- | --- | --- | --- | --- |
| Security (3) | 4 | 4 | 5 | 4 |
| Accessibility (3) | 5 | 3 | 4 | 4 |
| Code sharing (3) | 4 | 5 | 4 | 1 |
| Builder (2) | 5 | 3 | 3 | 5 |
| Team skills (2) | 3 | 3 | 3 | 1 |
| i18n (1) | 5 | 5 | 4 | 3 |
| Android build in Docker (1) | 4 | 4 | 4 | 4 |
| Ecosystem (1) | 5 | 3 | 4 | 4 |
| iOS bonus (1) | 5 | 5 | 4 | 5 |
| **Weighted total** | **74** | **65** | **67** | **55** |

Option A comes first, mainly thanks to accessibility and the builder. Team skills are equal for A, B and C, so they do not change the ranking. Even if accessibility and the builder were manageable in React Native Web (scores raised to 4), option B would only reach 70, still behind A at 74.

Rationale for the main scores:

- **Security**: React escapes content by default (XSS risk mostly comes from `dangerouslySetInnerHTML`). Angular adds built-in sanitization and XSRF support in its HTTP client. On mobile, React Native and Flutter both offer encrypted token storage (Android Keystore) and OAuth2 libraries with PKCE.
- **Accessibility**: semantic HTML (options A, C) is the easiest way to reach WCAG AA. React Native Web maps accessibility props to ARIA, but with less control.
- **Code sharing**: option B shares almost everything, option D nothing.
- **Builder**: React Flow (React DOM) and Flutter solutions are mature. In option B, the builder would be a separate web-only island.

## 5. Practical evidence (POCs)

Each POC must be committed to the repository under `poc/frontend/<option>/`, with a short README of the results.

| POC | Goal | Result |
| --- | --- | --- |
| A1 | login screen in React DOM, with EN/FR i18n, and axe / Lighthouse audit | to be completed |
| A2 | same login screen in React Native (Expo) on Android | to be completed |
| B1 | same login screen in RN Web + Android | to be completed |
| B2 | mini builder (3 nodes) in RN Web, React Flow in a `.web.tsx` file | to be completed |
| B3 | axe / Lighthouse audit of screen B1 on the web | score and issues found |
| C1 | same screen in Angular + Ionic, APK build | to be completed |
| D1 | same screen in Flutter, APK build | to be completed |
| X1 | APK build inside a Docker container for the selected option | to be completed |
| X2 | API client generated from a sample OpenAPI file | to be completed |
| X3 | shared package (types, API client, translations) imported by both a React and a React Native app | to be completed |

Questions the POCs must answer:

1. What accessibility gap do we measure between React DOM and RN Web on the same screen?
2. Can a shared package (types, API client, translations) be used by both React and React Native?
3. How long does it take to produce the APK in Docker?

## 6. Decision

**Choice: option A, React (web) + React Native with Expo (mobile).**

### Revision history

We first leaned towards option B (React Native Web + React Native) for its single codebase. The comparison showed that option A scores higher, even in the best case for option B (74 against 70). We therefore changed our decision before starting development.

### Reasons

- **Accessibility**: the web client is written in semantic HTML with React DOM, which is the most direct way to reach WCAG AA and to audit it with axe or Lighthouse.
- **Builder**: the whole React DOM ecosystem is available, including React Flow for a node editor.
- **Same language and concepts on both clients**: TypeScript, components, hooks. Any member can work on either client.
- **Code sharing is still possible**: a shared package holds the types and API client generated from the OpenAPI description, the i18n translation files and the validation rules.
- **iOS** stays reachable as a bonus through React Native, without a rewrite.

### Accepted consequences

- screens are written twice, once for the web and once for mobile. This is acceptable because the mobile client has a smaller scope: no builder, only listing, enabling, disabling and monitoring workflows;
- the shared package must be set up early (monorepo with npm or pnpm workspaces), so both clients use the same API client and translations;
- dependency on the Expo ecosystem for mobile builds.

### Rejected options

- **React Native Web + React Native**: rejected for this project because web accessibility and the builder are harder to deliver through the React Native abstraction layer. Its single codebase does not make up for that.
- **Angular + Ionic**: rejected because it scores lower and the mobile app would render in a WebView.
- **React + Flutter**: rejected because nothing could be shared between the clients and the team knows Flutter less.

This decision may still be revised if evidence invalidates it, and any change will be documented with its reason and consequences.