> **Status**: Created 2026-08-24 as part of Phase 5 intermediate scaffold.

# Plan — js-express intermediate scaffold

## Context

Build a minimal, working Express.js REST API scaffold that proves the template
works end-to-end: one real route, one passing test, CI green on push.

## Goals

1. Express app factory split from the server listener (testable in isolation)
2. One working route: `GET /health` returning `{ status: 'ok', timestamp }`
3. One passing Jest + supertest test for that route
4. GitHub Actions CI: `npm ci` + `npm test` on every push

## What was built

| File | Purpose |
|---|---|
| `src/app.js` | Express app + json/morgan middleware. No `listen()` — importable by tests. |
| `src/server.js` | Reads `PORT` from env, calls `app.listen()`. Entry point for `npm start`/`dev`. |
| `test/health.test.js` | supertest test: GET /health → 200 + `{ status: 'ok' }` |
| `package.json` | express, morgan, dotenv (runtime); jest, supertest, nodemon, eslint, prettier (dev) |
| `.nvmrc` | Pins Node 20 LTS |
| `.env.example` | PORT, NODE_ENV |
| `.github/workflows/test.yml` | CI: setup-node (from .nvmrc), npm ci, npm test |

## Verification steps

```bash
npm install
npm test          # 1 suite, 1 passing test
npm run dev       # server starts on port 3000
curl http://localhost:3000/health
# → {"status":"ok","timestamp":"<ISO string>"}
```

## Next steps

- Add centralised error-handling middleware and a 404 handler
- Add a real resource route (`/api/v1/<resource>`) with CRUD
- Wire ESLint + Prettier (eslint.config.js, .prettierrc)
- Add lint step to CI
