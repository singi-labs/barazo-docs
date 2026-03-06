<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/singi-labs/.github/main/assets/logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/singi-labs/.github/main/assets/logo-light.svg">
  <img alt="Barazo Logo" src="https://raw.githubusercontent.com/singi-labs/.github/main/assets/logo-dark.svg" width="120">
</picture>

# Barazo Docs

**Documentation site for the Barazo forum platform.**

[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange)]()
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/node-24%20LTS-brightgreen)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.x-blue)](https://www.typescriptlang.org/)

</div>

---

## Overview

Developer and admin documentation for [Barazo](https://github.com/singi-labs), hosted at [docs.barazo.forum](https://docs.barazo.forum). Built with [Fumadocs](https://fumadocs.vercel.app/) (Next.js). API reference is auto-generated from the OpenAPI spec; TypeScript type docs are auto-generated from lexicon source files.

---

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

---

## Documentation Sections

| Section            | Audience  | Description                                               |
| ------------------ | --------- | --------------------------------------------------------- |
| Getting Started    | Both      | Quickstart overview                                       |
| Self-Hosting       | Admin     | Requirements, installation, configuration, upgrading      |
| Admin Guide        | Admin     | Moderation, categories, customization, plugins            |
| API Reference      | Developer | Auto-generated from OpenAPI spec (interactive playground) |
| Lexicon Reference  | Developer | Auto-generated TypeScript type documentation              |
| AT Protocol        | Developer | AT Protocol concepts for Barazo                           |
| Plugin Development | Developer | Building and publishing plugins                           |
| Contributing       | Developer | Contributing to Barazo                                    |
| Migration          | Admin     | Migrating from other forum platforms                      |
| FAQ                | Both      | Frequently asked questions                                |

Audience-scoped sidebar tabs (Developer / Admin) provide separate navigation trees with scoped search.

---

## Quick Start

Prerequisites: Node.js 24 LTS, pnpm.

```bash
git clone https://github.com/singi-labs/barazo-docs.git
cd barazo-docs
pnpm install
pnpm dev
```

---

## Development

```bash
pnpm dev          # Start dev server
pnpm build        # Static export
pnpm lint         # ESLint
pnpm typecheck    # TypeScript strict mode
```

See [CONTRIBUTING.md](https://github.com/singi-labs/.github/blob/main/CONTRIBUTING.md) for contribution guidelines.

**Key standards:**

- Strict TypeScript -- `strict: true`, no `any`, no `@ts-ignore`
- WCAG 2.2 AA accessibility from first commit
- Static export -- all pages pre-rendered at build time
- Auto-generated docs rebuild when barazo-api or barazo-lexicons update

---

## Auto-Generated Content

Two categories of documentation are generated at build time rather than written by hand:

**API Reference** -- The Barazo API (barazo-api) generates an OpenAPI spec from its Zod validation schemas via `@fastify/swagger`. The `fumadocs-openapi` package converts this spec into interactive documentation pages with parameter tables, request/response schemas, code samples, and a live API playground.

**Lexicon Type Docs** -- The `fumadocs-typescript` package reads TypeScript type definitions from barazo-lexicons and generates type documentation tables. Changes to lexicon schemas automatically update the docs on the next build.

---

## Related Repositories

| Repository                                                         | Description                                        | License     |
| ------------------------------------------------------------------ | -------------------------------------------------- | ----------- |
| [barazo-api](https://github.com/singi-labs/barazo-api)             | AppView backend (Fastify, PostgreSQL, AT Protocol) | AGPL-3.0    |
| [barazo-web](https://github.com/singi-labs/barazo-web)             | Forum frontend (Next.js, TailwindCSS)              | MIT         |
| [barazo-lexicons](https://github.com/singi-labs/barazo-lexicons)   | AT Protocol schemas for forum data                 | MIT         |
| [barazo-deploy](https://github.com/singi-labs/barazo-deploy)       | Docker Compose templates for self-hosting          | MIT         |
| [barazo-website](https://github.com/singi-labs/barazo-website)     | Marketing site (Astro)                             | Proprietary |
| [barazo-workspace](https://github.com/singi-labs/barazo-workspace) | Project coordination and shared tooling            | MIT         |

---

## Community

- **Website:** [barazo.forum](https://barazo.forum)
- **Discussions:** [GitHub Discussions](https://github.com/orgs/singi-labs/discussions)
- **Issues:** [Report bugs](https://github.com/singi-labs/barazo-docs/issues)

---

## License

This repository uses a dual license:

**Content** (MDX documentation files in `content/`): **CC BY-SA 4.0**

**Code** (Fumadocs configuration, components, layouts, build scripts): **MIT**

See [LICENSE](LICENSE) for the content license and [LICENSE-CODE](LICENSE-CODE) for the code license.

---

(c) 2026 Barazo
