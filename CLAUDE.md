# CLAUDE.md — js-express

This is the **Node.js + Express template** of the `coding-project-templates` library. It lives on branch `web-js` and is checked out as a git worktree at `features/js-express` within the root repo.

> **Note:** This is a Node.js project, not Python. The root repo uses Python tooling (`uv`, `.venv`, `pyproject.toml`) — none of that applies here. Use `npm` and `.nvmrc` for this template.

## Stack

- **Runtime**: Node.js 20 LTS (pinned in `.nvmrc`)
- **Framework**: Express 4
- **Logging**: morgan
- **Testing**: Jest + supertest
- **Dev tooling**: nodemon, ESLint, Prettier

## Project layout

```
src/
  app.js       ← Express app factory (no listen call — importable by tests)
  server.js    ← Entry point: reads PORT, calls app.listen()
  routes/      ← Add route files here (import into app.js)
test/
  *.test.js    ← Jest + supertest tests
.github/
  workflows/
    test.yml   ← CI: npm ci + npm test
```

## npm Scripts

| Command | What it does |
|---|---|
| `npm start` | Run server (production) |
| `npm run dev` | nodemon — auto-restart on save |
| `npm test` | Jest with coverage |
| `npm run lint` | ESLint over src/ and test/ |

## Key patterns

**App factory** — `src/app.js` exports the Express app without calling `.listen()`. This lets `supertest` import it directly without binding a port:

```javascript
// test/my.test.js
const request = require('supertest');
const app = require('../src/app');
const res = await request(app).get('/my-route');
```

**Adding a route**:
```javascript
// src/routes/things.js
const router = require('express').Router();
router.get('/', (req, res) => res.json({ things: [] }));
module.exports = router;

// src/app.js
app.use('/things', require('./routes/things'));
```

## Repo conventions (from root CLAUDE.md)

- **Commits** on this branch: `feat: <what changed>` or `fix: <what changed>`
- **Push** to `origin web-js` from inside this worktree
- **Planning notes** live in the root repo's `claude/` folder (numbered `N-Title.md`), not here
- **GitHub Project**: [Wema-Digital/projects/2](https://github.com/orgs/Wema-Digital/projects/2) — mark tasks Done after committing

## Receiving base updates

```bash
cd features/js-express   # branch web-js
git merge claude-code-b
git push origin web-js
```
