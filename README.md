# js-express — Express.js REST Starter Template

> The Node.js/JavaScript counterpart to the Python web templates in this library.
> Clone, install, and have a running Express API with tests and CI in minutes.

---

## Quick Start

```bash
# 1. Use the right Node version (requires nvm)
nvm use

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env

# 4. Start the dev server (auto-reloads on change)
npm run dev

# 5. Verify it's running
curl http://localhost:3000/health
# → {"status":"ok","timestamp":"..."}
```

---

## Project Layout

```
js-express/
├── src/
│   ├── app.js          # Express app + middleware (no listen — testable in isolation)
│   └── server.js       # Binds the app to a port; entry point for npm start/dev
├── test/
│   └── health.test.js  # Jest + supertest example test
├── .env.example        # Environment variable template — copy to .env
├── .nvmrc              # Pinned Node version (Node 20 LTS)
├── package.json        # Dependencies + npm scripts
├── CLAUDE.md           # Claude Code context for this template
└── todo.md             # Task tracking template (symbol system)
```

---

## npm Scripts

| Command | What it does |
|---|---|
| `npm start` | Run the server (production mode) |
| `npm run dev` | Run with nodemon — auto-restart on file change |
| `npm test` | Run Jest test suite with coverage |
| `npm run lint` | ESLint across `src/` and `test/` |

---

## Adding Routes

Keep the app factory pattern — add new routes/routers to `src/app.js`:

```javascript
// src/routes/users.js
const router = require('express').Router();
router.get('/', (req, res) => res.json({ users: [] }));
module.exports = router;

// src/app.js
const usersRouter = require('./routes/users');
app.use('/users', usersRouter);
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `PORT` | `3000` | Port the server listens on |
| `NODE_ENV` | `development` | `development` \| `production` \| `test` |

Copy `.env.example` to `.env` and fill in values. Never commit `.env`.

---

## Testing

Tests use [Jest](https://jestjs.io/) + [supertest](https://github.com/ladjs/supertest).
`supertest` imports `app.js` directly (no running server needed), so tests are fast and port-independent.

```bash
npm test               # run all tests + coverage report
npm test -- --watch    # watch mode during development
```

---

## Working with Claude Code

This template follows the same `todo.md` task-tracking convention as `claude-code-basic`.
See `todo.md` for the full symbol system and task breakdown.

Useful prompts to get started:
- *"Read todo.md and help me add a new route with tests."*
- *"Review my Express middleware setup against best practices."*
- *"Add input validation with express-validator to the POST /users route."*

---

**Template Version**: 1.0
**Last Updated**: 2026-08-24
**Branch**: `web-js` | **Stack**: Node.js 20 + Express 4 + Jest
