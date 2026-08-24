# Todo — js-express

> Express.js REST API project tasks. Uses the same symbol system as the base template.
> See the Symbol Guide below for reference.

## Symbol Guide

| Symbol | Meaning | When to use with Claude |
|--------|---------|-------------------------|
| `[ ]` | Unstarted | Default for all new tasks |
| `[x]` | Completed | Ask Claude to mark tasks done |
| `[-]` | In-progress | Claude marks what it's actively working on |
| `[!]` | High priority | Focus here first |
| `[@]` | Needs discussion | Ask Claude for design input |
| `[?]` | Needs research | Have Claude research options |
| `[#]` | Medium priority | After `[!]` tasks |
| `[~]` | On hold | Skip for now |
| `[>]` | Delegated/deferred | Assigned elsewhere or future |
| `[⚠]` | Critical issue | Urgent bug or blocker |
| `[%]` | % complete | Track large in-progress features |

---

## Project Setup

```markdown
- [x] [!] Initialise git repository and branch (web-js)
- [x] [!] Create package.json with express, morgan, dotenv
- [x] [!] Add dev deps: jest, supertest, nodemon, eslint, prettier
- [x] [!] Pin Node version in .nvmrc (.nvmrc = 20)
- [x] Configure .env.example (PORT, NODE_ENV)
- [x] Update .gitignore for Node (node_modules, .env, coverage/)
- [ ] [@] Decide on folder structure for routes (flat vs. feature-based)
- [ ] [#] Configure ESLint (eslint.config.js)
- [ ] [#] Configure Prettier (.prettierrc)
```

---

## Core Routes & Middleware

```markdown
- [x] [!] GET /health — baseline health-check route
- [ ] [!] Centralised error-handling middleware (err, req, res, next)
- [ ] [!] 404 handler (catch-all after all routes)
- [ ] [#] Request logging with morgan (already wired in app.js)
- [ ] [@] Decide on API versioning strategy (/api/v1/...)
- [ ] [ ] Add your first real resource route:
  - [ ] GET    /api/v1/<resource>      — list
  - [ ] POST   /api/v1/<resource>      — create
  - [ ] GET    /api/v1/<resource>/:id  — get one
  - [ ] PUT    /api/v1/<resource>/:id  — update
  - [ ] DELETE /api/v1/<resource>/:id  — delete
- [ ] [#] Input validation middleware (express-validator or zod)
- [ ] [~] Rate limiting (express-rate-limit) for public endpoints
```

---

## Configuration & Environment

```markdown
- [x] [!] Load env vars with dotenv in server.js
- [ ] [#] Centralise config in src/config.js (read from process.env)
- [ ] [@] Decide on secrets strategy (env vars vs. a secrets manager)
- [ ] [ ] Document all required env vars in .env.example
```

---

## Testing

```markdown
- [x] [!] Setup Jest + supertest
- [x] [!] test/health.test.js — GET /health passing test
- [ ] [!] Write tests for each new route (happy path + error cases)
- [ ] [#] Test error-handling middleware
- [ ] [#] Test 404 handler
- [ ] [% 0] Reach 80% test coverage
- [ ] [@] Discuss integration vs. unit test split strategy
```

**Claude Code for testing:**
```markdown
- [ ] [!] Ask Claude to generate tests for any new route added above
- [ ] [#] Have Claude review test coverage report and suggest gaps
```

---

## CI / Deployment

```markdown
- [x] [!] .github/workflows/test.yml — npm ci + npm test on every push
- [ ] [#] Add lint step to CI (npm run lint)
- [ ] [@] Choose hosting platform (Railway, Render, Fly.io, AWS, etc.)
- [ ] [ ] Add deployment workflow
- [ ] [~] Dockerise (Dockerfile + .dockerignore)
- [ ] [>] Setup staging environment
```

---

## Code Quality

```markdown
- [ ] [#] Configure ESLint (eslint.config.js)
- [ ] [#] Configure Prettier (.prettierrc)
- [ ] [~] Add pre-commit hooks (husky + lint-staged)
- [ ] [ ] Add JSDoc comments to public functions
```

---

## Metadata

*Last Updated: 2026-08-24*
*Template Version: 1.0*
*Stack: Node.js 20 + Express 4 + Jest + supertest*
