# Barazo Docs -- Documentation Site

<!-- Auto-generated from barazo-workspace. To propose changes, edit the source:
     https://github.com/barazo-forum/barazo-workspace/tree/main/agents-md -->

MIT | Part of [github.com/barazo-forum](https://github.com/barazo-forum)

Documentation site for Barazo at docs.barazo.forum. Built with Fumadocs (Next.js).

## Tech Stack

| Component  | Technology                                           |
| ---------- | ---------------------------------------------------- |
| Framework  | Fumadocs (Next.js 16 / React 19 / TypeScript strict) |
| Styling    | TailwindCSS                                          |
| API docs   | fumadocs-openapi (auto-generated from OpenAPI spec)  |
| Type docs  | fumadocs-typescript (auto-generated from source)     |
| Search     | Orama (self-hosted, audience-scoped)                 |
| Icons      | Phosphor Icons                                       |
| Typography | Source Sans 3 / Source Code Pro (self-hosted)        |
| Output     | Static export (zero server runtime)                  |

## What This Repo Does

- Developer documentation (API reference, plugin dev guide, lexicon reference, AT Protocol concepts, contributing guide)
- Admin documentation (self-hosting guide, admin guide, FAQ, migration guides)
- API reference auto-generated from OpenAPI spec via fumadocs-openapi
- TypeScript type documentation auto-generated from lexicon types via fumadocs-typescript
- Audience-scoped navigation (Developer / Admin sidebar tabs)
- Shared header/footer via @barazo/ui-shell (React build)
- LLM-friendly docs output (llms.txt)

## Docs-Specific Standards

- Strict TypeScript -- `strict: true`, no `any`, no `@ts-ignore`
- Accessibility -- WCAG 2.2 AA, semantic HTML
- Static export -- all pages pre-rendered at build time, zero client JS where possible
- Search -- Orama (self-hosted), no external SaaS dependencies
- Auto-generation -- API docs and type docs must rebuild when barazo-api or barazo-lexicons update

---

## Project-Wide Standards

### About Barazo

Open-source forum software built on the [AT Protocol](https://atproto.com/). Portable identity, member-owned data, no lock-in.

- **Organization:** [github.com/barazo-forum](https://github.com/barazo-forum)
- **License:** AGPL-3.0 (backend) / MIT (frontend, lexicons, deploy) / CC BY-SA 4.0 + MIT (docs) / Proprietary (website)
- **Contributing:** See [CONTRIBUTING.md](https://github.com/barazo-forum/.github/blob/main/CONTRIBUTING.md)

### Coding Standards

1. **Test-Driven Development** -- write tests before implementation (Vitest).
2. **Strict TypeScript** -- `strict: true`, no `any`, no `@ts-ignore`.
3. **Conventional commits** -- `type(scope): description`.
4. **CI must pass** -- lint, typecheck, tests, security scan on every PR.
5. **Input validation** -- Zod schemas on all API inputs and firehose records.
6. **Output sanitization** -- DOMPurify on all user-generated content.
7. **No raw SQL** -- Drizzle ORM with parameterized queries only.
8. **Structured logging** -- Pino logger, never `console.log`.

### Git Workflow

All changes go through Pull Requests -- never commit directly to `main`. Branch naming: `type/short-description` (e.g., `feat/add-reactions`, `fix/xss-sanitization`).

### AT Protocol Context

- Users own their data (stored on their Personal Data Server)
- The AppView (barazo-api) indexes data from the AT Protocol firehose
- Lexicons (`forum.barazo.*`) define the data schema contract
- Identity is portable via DIDs -- no vendor lock-in
- All record types are validated against lexicon schemas
