# Todo Template for Software Development Projects

> A comprehensive task tracking template for any programming language or framework.
> Works seamlessly with Claude Code for AI-assisted development.

## Symbol Guide

| Symbol | Meaning                   | Example Use Case                    |
|--------|---------------------------|-------------------------------------|
| `[ ]`  | Unstarted task            | `- [ ] Create project structure`    |
| `[x]`  | Completed task            | `- [x] Setup CI/CD pipeline`        |
| `[-]`  | In-progress               | `- [-] Implementing user auth`      |
| `[~]`  | On hold                   | `- [~] Performance optimization`    |
| `[>]`  | Delegated/postponed       | `- [>] Design system review`        |
| `[!]`  | High priority             | `- [!] Fix critical bug`            |
| `[?]`  | Needs research            | `- [?] Best caching strategy`       |
| `[@]`  | Requires discussion       | `- [@] API design approach`         |
| `[$]`  | Budget-related            | `- [$] Cloud hosting costs`         |
| `[#]`  | Medium priority           | `- [#] Update documentation`        |
| `[%]`  | Percentage completed      | `- [% 60] Integration tests`        |
| `[→]`  | Moved to another section  | `- [→] Moved to maintenance`        |
| `[⚠]`  | Critical issue            | `- [⚠] Security vulnerability`      |

This template maintains compatibility with GitHub/GitLab rendering while adding enhanced task management features for:

- Multi-language project development
- Feature planning and implementation
- Code quality and testing workflows
- DevOps and deployment tracking
- Collaboration with Claude Code AI assistant
- Progress monitoring and team coordination

**Working with Claude Code:**

When using this template with Claude Code, you can:
- Ask Claude to read this file and suggest next tasks
- Reference specific tasks in your prompts (e.g., "Complete the [!] task in Project Setup")
- Request Claude to update task statuses as work progresses
- Use [@] markers to flag items where you need Claude's input on approach
- Track percentage completion with [%] for incremental features

## Customization Guide

```markdown
1. **Priority Mapping**
   `(!) → High | (#) → Medium | ( ) → Low`

2. **Status Indicators**
   Combine symbols: `- [x][!] Completed security patch`

3. **Progress Tracking**
   Use percentages: `- [% 85] Feature implementation`

4. **Team Coordination**
   `(@) = Discussion needed | (>) = Delegated to team member`

5. **Custom Symbols**
   Add project-specific markers:

| Custom Symbol | Meaning                    |
|---------------|----------------------------|
| `[🚀]`         | Deployment related         |
| `[📝]`         | Documentation needed       |
| `[🔧]`         | Configuration/setup        |
| `[🎨]`         | UI/UX work                 |
| `[🔒]`         | Security related           |
| `[⚡]`         | Performance improvement    |
| `[🧪]`         | Testing/QA                 |
```

---

## Project Setup & Planning

Essential tasks for initializing your project:

```markdown
- [ ] [!] Initialize version control (git repository)
- [ ] [@] Define project requirements and scope
- [ ] [ ] Choose technology stack:
  - [ ] Programming language(s)
  - [ ] Framework(s) and libraries
  - [ ] Database system (if needed)
  - [ ] Development tools and IDE
- [ ] [🔧] Setup development environment:
  - [ ] Install dependencies
  - [ ] Configure build tools
  - [ ] Setup environment variables (.env files)
  - [ ] Create project structure (src/, tests/, docs/)
- [ ] [#] Document architecture decisions
- [ ] [@] Establish coding standards and style guide
- [ ] [$] Evaluate third-party service costs
- [ ] [>] Setup project management tools (Jira, Linear, etc.)
```

**Example with Claude Code:**
```markdown
- [x] Initialize git repository
- [-] [!] Setup project dependencies    # Claude is currently helping with this
- [ ] [@] Decide on state management    # Need to discuss Redux vs Context API
```

---

## Core Development

Feature implementation and core functionality:

### Feature: User Authentication
```markdown
- [ ] [!] Design authentication flow
- [ ] [ ] Implement user registration:
  - [ ] Create registration form/endpoint
  - [ ] Validate user input
  - [ ] Hash passwords securely
  - [ ] Store user data
- [ ] [-] [#] Build login functionality
- [ ] [?] Research OAuth integration options
- [ ] [@] Discuss session vs JWT approach
- [ ] [% 30] Password reset feature
```

### Feature: Core Application Logic
```markdown
- [ ] [!] Implement main business logic
- [ ] [ ] Create data models/schemas
- [ ] [🔧] Setup database connections
- [ ] [ ] Build API endpoints/interfaces:
  - [ ] [!] Create resource endpoint
  - [ ] [#] Update resource endpoint
  - [ ] [ ] Delete resource endpoint
  - [ ] [ ] List/search endpoints
- [ ] [~] Add pagination support
- [ ] [>] Implement advanced filtering
```

### Feature: User Interface (if applicable)
```markdown
- [ ] [🎨] Design component architecture
- [ ] [ ] Build reusable UI components:
  - [ ] Button component
  - [ ] Form input components
  - [ ] Navigation components
  - [ ] Modal/dialog components
- [ ] [-] [!] Implement responsive layouts
- [ ] [% 50] Add loading states and error handling
- [ ] [@] Discuss accessibility requirements
```

**Claude Code Tips:**
- Break features into small, atomic tasks that Claude can complete in one session
- Use [!] for tasks that Claude should prioritize
- Mark [?] items to ask Claude for research and recommendations
- Track [%] completion for large features Claude is building incrementally

---

## Code Quality & Documentation

Maintaining clean, documented code:

```markdown
- [ ] [!] Setup linting and formatting:
  - [ ] Configure linter (ESLint, Pylint, Clippy, etc.)
  - [ ] Add format tool (Prettier, Black, rustfmt, etc.)
  - [ ] Create pre-commit hooks
- [ ] [@] Establish code review process
- [ ] [ ] Write technical documentation:
  - [ ] [📝] Architecture overview
  - [ ] [📝] API documentation
  - [ ] [📝] Setup instructions
  - [ ] [📝] Contribution guidelines
- [ ] [#] Add inline code comments
- [ ] [% 40] Type annotations/hints (if applicable)
- [ ] [~] Refactor legacy code sections
- [ ] [>] Peer review requested for auth module
```

**Working with Claude:**
```markdown
- [x] [@] Asked Claude to explain complex algorithm in api/utils.js:145
- [-] [📝] Having Claude generate API documentation from code
- [ ] [!] Request Claude to refactor error handling patterns
```

---

## Testing & Quality Assurance

Ensuring reliability and correctness:

```markdown
- [ ] [!] Setup testing framework:
  - [ ] Choose test runner (Jest, pytest, cargo test, etc.)
  - [ ] Configure test environment
  - [ ] Setup code coverage tools
- [ ] [ ] Write unit tests:
  - [ ] [!] Test authentication logic
  - [ ] [#] Test business logic functions
  - [ ] [% 55] Test utility functions
  - [ ] [ ] Test edge cases
- [ ] [🧪] Create integration tests:
  - [ ] Test API endpoints
  - [ ] Test database operations
  - [ ] Test external service integrations
- [ ] [~] Implement end-to-end tests
- [ ] [⚠] Fix failing test in payment module
- [ ] [@] Discuss test coverage goals (80%? 90%?)
- [ ] [?] Research property-based testing
```

**Bug Tracking:**
```markdown
- [ ] [⚠] Critical: Login fails with special characters in password
- [ ] [!] High: Memory leak in file upload handler
- [ ] [#] Medium: UI glitch on mobile devices
- [ ] [ ] Low: Inconsistent button styling
```

**Claude Code for Testing:**
```markdown
- [x] Asked Claude to generate unit tests for validator.js
- [-] [% 70] Claude writing integration tests for API endpoints
- [ ] [!] Have Claude fix the failing authentication test
```

---

## Deployment & DevOps

Production readiness and operations:

```markdown
- [ ] [!] Setup CI/CD pipeline:
  - [ ] [🚀] Configure build automation
  - [ ] [🧪] Add automated testing in CI
  - [ ] [🚀] Setup deployment automation
  - [ ] [ ] Configure deployment environments
- [ ] [@] Choose hosting platform:
  - [ ] [$] Evaluate costs (AWS, GCP, Azure, Vercel, etc.)
  - [ ] [?] Research scaling requirements
  - [ ] [ ] Compare feature sets
- [ ] [🔧] Environment configuration:
  - [ ] [!] Setup production environment variables
  - [ ] [#] Configure staging environment
  - [ ] [ ] Setup development environment
- [ ] [🔒] [!] Security hardening:
  - [ ] Enable HTTPS/TLS
  - [ ] Configure firewall rules
  - [ ] Setup secrets management
  - [ ] Enable DDoS protection
- [ ] [ ] Implement monitoring and logging:
  - [ ] [!] Setup error tracking (Sentry, etc.)
  - [ ] [#] Configure application logging
  - [ ] [ ] Setup performance monitoring (APM)
  - [ ] [ ] Create alerting rules
- [ ] [>] Setup container orchestration (Docker/Kubernetes)
- [ ] [% 25] Database backup and recovery procedures
```

**Deployment Checklist:**
```markdown
- [ ] [!] Run full test suite
- [ ] [!] Update version numbers
- [ ] [📝] Write release notes
- [ ] [🚀] Deploy to staging
- [ ] [🧪] QA testing on staging
- [ ] [@] Get deployment approval
- [ ] [🚀] Deploy to production
- [ ] [!] Monitor for errors post-deployment
```

---

## Maintenance & Optimization

Ongoing improvements and upkeep:

```markdown
- [ ] [⚡] Performance optimization:
  - [ ] [?] Profile application performance
  - [ ] [!] Optimize slow database queries
  - [ ] [#] Reduce bundle size
  - [ ] [ ] Implement caching strategies
  - [ ] [% 45] Add lazy loading for images
- [ ] [🔒] Security updates:
  - [ ] [⚠] Patch critical vulnerability in dependency
  - [ ] [!] Update authentication library
  - [ ] [#] Run security audit
  - [ ] [ ] Update SSL certificates
- [ ] [🔧] Dependency management:
  - [ ] [#] Update minor version dependencies
  - [ ] [~] Research migration to new framework version
  - [ ] [@] Discuss removing unused dependencies
- [ ] [~] Technical debt reduction:
  - [ ] [>] Refactor monolithic module
  - [ ] [ ] Replace deprecated API calls
  - [ ] [#] Improve error handling consistency
- [ ] [@] Backward compatibility considerations
- [ ] [$] Cost optimization review
```

**Monitoring Tasks:**
```markdown
- [ ] [!] Investigate spike in error rates
- [ ] [#] Review performance metrics
- [ ] [ ] Analyze user feedback
- [ ] [⚠] Critical: Database running out of disk space
```

---

## Notes & Ideas

Use this section for brainstorming and tracking ideas:

```markdown
- [ ] [?] Consider implementing GraphQL API
- [ ] [💡] Idea: Add dark mode toggle
- [ ] [@] Discuss: Should we add real-time features?
- [ ] [~] Maybe: Mobile app version
- [ ] [>] Future: AI-powered recommendations
```

---

## Metadata

*Last Updated: 2026-02-12*
*Template Version: 3.0*
*Applicable to: Any programming language/framework*

**Customization Notes:**
- Adapt sections based on your project type (web app, CLI tool, library, API, etc.)
- Remove or add sections as needed (e.g., mobile-specific, data pipeline, game dev)
- Customize emoji symbols to match your team's workflow
- Integrate with your existing project management tools
- Use with Claude Code for AI-assisted development and task tracking

**Language-Specific Variations:**
- Web: Add frontend/backend separation, API versioning
- CLI Tools: Add command design, argument parsing, installation tasks
- Libraries: Add API design, versioning, documentation generation
- Mobile: Add platform-specific tasks (iOS, Android), app store deployment
- Data Science: Add data pipeline, model training, experiment tracking

**Claude Code Integration:**
For best results when using this template with Claude Code:
1. Share this file with Claude at the start of your project
2. Ask Claude to read it periodically to stay aligned with priorities
3. Request Claude to update task statuses as work completes
4. Use [@] markers to request Claude's input on architectural decisions
5. Reference specific tasks in your prompts for focused work sessions
