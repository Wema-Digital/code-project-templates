# Claude Code Project Template

> A language-agnostic starter template for building any software project with Claude Code.
> Jump-start your development with structured task tracking and AI-assisted coding.

## Overview

This template provides a comprehensive foundation for starting any software development project with Claude Code - Anthropic's AI coding assistant. Whether you're building a web application, CLI tool, mobile app, API service, or data pipeline, this template gives you the structure and workflow to develop efficiently with AI assistance.

**What makes this template special:**
- ✅ **Language-agnostic**: Works with Python, JavaScript, Go, Rust, Java, or any language
- ✅ **Claude Code optimized**: Designed for AI-assisted development workflows
- ✅ **Comprehensive task tracking**: Symbol-based system for managing complex projects
- ✅ **Ready to use**: Clone and start coding immediately

---

## Quick Start

### 1. Get This Template

```bash
# Clone this repository
git clone <repository-url> my-new-project
cd my-new-project

# Remove the template's git history (optional)
rm -rf .git
git init
```

### 2. Customize for Your Language

**For Python projects:**
```bash
# Keep requirements.txt and install dependencies
pip install -r requirements.txt

# Or use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**For JavaScript/Node.js projects:**
```bash
# Replace requirements.txt with package.json
npm init -y
npm install --save-dev jest dotenv

# Create your package.json with your dependencies
```

**For Go projects:**
```bash
# Replace requirements.txt with go.mod
go mod init github.com/yourusername/project-name
```

**For Rust projects:**
```bash
# Replace requirements.txt with Cargo.toml
cargo init
```

**For other languages:** See the [Customization Guide](#customization-guide) below.

### 3. Start Working with Claude Code

1. Open `todo.md` in your editor
2. Customize the template tasks for your specific project
3. Start a Claude Code session and say:
   > "Hi Claude, I'm starting a new [project type] project. Please read todo.md to understand the structure, then help me with the [!] high priority tasks in the Project Setup section."

---

## What's Included

### 📋 `todo.md` - Comprehensive Task Tracking Template

A sophisticated task management system with:
- **Symbol-based status tracking**: 13 different status markers ([ ], [x], [!], [@], etc.)
- **Pre-structured sections**: Project Setup, Core Development, Testing, Deployment, Maintenance
- **Detailed examples**: Learn by seeing real task entries with different symbols
- **Claude Code integration tips**: Guidance on using each section with AI assistance

**Perfect for:**
- Breaking down features into manageable chunks
- Tracking progress across complex projects
- Coordinating with Claude Code on what to build next
- Prioritizing high-impact work

### 📚 `README.md` - This Guide

Instructions for using this template effectively with Claude Code, customization options, and best practices.

### 📦 `requirements.txt` - Example Dependencies

Python dependencies as a starting point. Includes:
- `pytest` - Testing framework
- `python-dotenv` - Environment variable management
- `pandas` - Data manipulation

**For other languages**: Replace with your language's dependency file (see comments in file).

### 🙈 `.gitignore`

Standard patterns for ignoring common files (dependencies, build artifacts, environment files, etc.).

---

## Working with Claude Code

This template is optimized for AI-assisted development. Here's how to get the most out of Claude Code:

### Task Breakdown Strategy

**Break large features into Claude-friendly chunks:**

❌ **Too Large:**
```markdown
- [ ] Build complete user authentication system
```

✅ **Just Right:**
```markdown
- [ ] Design authentication flow and data models
- [ ] Implement user registration endpoint
- [ ] Add password hashing with bcrypt
- [ ] Create login endpoint with JWT generation
- [ ] Build password reset functionality
- [ ] Write authentication middleware
- [ ] Add unit tests for auth functions
```

**Why this matters:** Claude works best with focused, atomic tasks. Breaking work into 30-minute chunks allows Claude to complete tasks fully in one session.

### Effective Prompting

**Reference todo.md tasks in your prompts:**

✅ **Good prompts:**
- "Complete the [!] high priority task in Project Setup about initializing version control"
- "Work on the User Authentication feature in Core Development. Start with the registration endpoint task."
- "I see a [@] discussion marker on API design. Can you explain the tradeoffs between REST and GraphQL for this project?"
- "The deployment checklist has a [⚠] critical issue. Help me investigate and fix it."

❌ **Less effective:**
- "Build some features" (too vague)
- "Do whatever you think is next" (Claude can't prioritize without context)

### Iterative Development Workflow

**1. Planning Phase:**
```markdown
You: "Read todo.md and suggest which tasks we should tackle first based on dependencies."

Claude: [Analyzes todo.md and suggests starting with Project Setup tasks]

You: "Great, let's start with [!] initializing version control. Mark it as in-progress in todo.md."
```

**2. Implementation Phase:**
```markdown
You: "Implement the user registration endpoint as described in Core Development."

Claude: [Writes code, tests, documentation]

You: "Update todo.md to mark that task as completed and move to the next one."
```

**3. Review Phase:**
```markdown
You: "Review the authentication code we wrote against the requirements in todo.md."

Claude: [Performs code review, suggests improvements]
```

### Status Tracking with Claude

**Ask Claude to maintain todo.md as you work together:**

```markdown
You: "As we complete tasks, please update the status markers in todo.md. Use:
- [x] for completed tasks
- [-] for what you're currently working on
- [!] to flag anything that needs my immediate attention"

Claude: "I'll keep todo.md updated as we progress..."
```

**Pro tip:** Periodically ask Claude to read todo.md to stay aligned with project priorities.

### Code Review with Claude

**Use Claude to review completed work:**

```markdown
You: "The auth module is done. Review it against these criteria from todo.md:
- [✓] Password hashing implemented correctly
- [✓] Input validation on all endpoints
- [✓] Unit tests written
- [ ] Integration tests written

What's missing?"

Claude: [Reviews code and identifies integration tests need attention]
```

### Documentation Generation

**Have Claude document as it codes:**

```markdown
You: "While implementing the API endpoints, please add:
- Docstrings for all functions
- Inline comments for complex logic
- Update todo.md's documentation section with completion status"
```

### Best Practices for Claude Code Development

#### ✅ DO:
- **Keep tasks atomic**: One clear outcome per task
- **Use specific symbols**: [!] for urgent, [@] for discussion needed, [?] for research required
- **Reference file paths**: "Update the authentication logic in src/auth/login.js:45"
- **Ask Claude to update todo.md**: "Mark this task as complete in todo.md"
- **Provide context**: Share relevant parts of todo.md when starting new features

#### ❌ DON'T:
- **Give vague instructions**: "Make it better" or "Add features"
- **Skip task breakdown**: Large tasks are harder for Claude to complete fully
- **Forget to update status**: Keep todo.md current so Claude knows what's done
- **Mix multiple features**: Focus on one feature/task at a time

---

## Symbol System Quick Reference

| Symbol | Meaning | When to Use with Claude |
|--------|---------|-------------------------|
| `[ ]` | Unstarted | Default for all new tasks |
| `[x]` | Completed | Ask Claude to mark tasks done |
| `[-]` | In-progress | Claude should mark tasks it's actively working on |
| `[!]` | High priority | Tell Claude to focus here first |
| `[@]` | Needs discussion | Ask Claude for architecture/design input |
| `[?]` | Needs research | Have Claude research and recommend approaches |
| `[#]` | Medium priority | Work on after [!] tasks |
| `[~]` | On hold | Don't work on these yet |
| `[>]` | Delegated | Tasks assigned to team members or postponed |
| `[$]` | Budget-related | Requires cost evaluation |
| `[%]` | % complete | Track progress on large features (e.g., `[% 60]`) |
| `[⚠]` | Critical issue | Urgent bugs or problems needing immediate attention |
| `[→]` | Moved | Task relocated to different section |

**Pro tips:**
- Combine symbols: `[x][!]` = "Completed high-priority task"
- Use [@] when you want Claude's input before proceeding
- Use [?] when you want Claude to research options
- Use [%] for features Claude is building incrementally

See `todo.md` for complete documentation and examples.

---

## Customization Guide

### For Different Programming Languages

#### Python
```bash
# Already configured! Keep requirements.txt
pip install -r requirements.txt

# Add to requirements.txt as needed:
# flask>=3.0.0  # Web framework
# sqlalchemy>=2.0.0  # Database ORM
# requests>=2.31.0  # HTTP library
```

#### JavaScript/Node.js
```bash
# Replace requirements.txt with package.json
npm init -y

# Install common dependencies
npm install --save-dev jest eslint prettier
npm install dotenv express  # Example: for web apps

# Update todo.md to reference npm/node tools
```

#### TypeScript
```bash
npm init -y
npm install --save-dev typescript @types/node jest ts-jest
npx tsc --init

# Configure tsconfig.json for your project
```

#### Go
```bash
# Replace requirements.txt with go.mod
go mod init github.com/username/project

# Add dependencies as you use them
go get github.com/gorilla/mux  # Example: web framework
```

#### Rust
```bash
# Replace requirements.txt with Cargo.toml
cargo init

# Add dependencies to Cargo.toml:
# [dependencies]
# serde = { version = "1.0", features = ["derive"] }
# tokio = { version = "1", features = ["full"] }
```

#### Java
```bash
# Replace requirements.txt with pom.xml (Maven)
mvn archetype:generate -DgroupId=com.yourcompany -DartifactId=project

# Or build.gradle (Gradle)
gradle init --type java-application
```

#### Ruby
```bash
# Replace requirements.txt with Gemfile
bundle init

# Add to Gemfile:
# gem 'rspec'
# gem 'dotenv'
```

#### C# / .NET
```bash
# Replace requirements.txt with .csproj
dotnet new console -n ProjectName
cd ProjectName

# Add packages:
# dotnet add package Newtonsoft.Json
```

### For Different Project Types

#### Web Application (Frontend + Backend)
```markdown
Customize todo.md:
- Add "Frontend Development" section (components, routing, state management)
- Add "Backend Development" section (API endpoints, database, auth)
- Add "API Design" section (REST/GraphQL schema, versioning)
- Update deployment section for web hosting (Vercel, Netlify, AWS, etc.)
```

#### CLI Tool
```markdown
Customize todo.md:
- Add "Command Design" section (argument parsing, subcommands, help text)
- Add "Installation" section (package managers, distribution)
- Add "User Experience" section (error messages, progress indicators)
- Update testing section for CLI-specific tests
```

#### Library/Package
```markdown
Customize todo.md:
- Add "Public API Design" section (exported functions, backwards compatibility)
- Add "Documentation" section (API docs, usage examples, README)
- Add "Versioning Strategy" section (semantic versioning, changelog)
- Add "Publishing" section (npm, PyPI, crates.io, etc.)
```

#### API/Microservice
```markdown
Customize todo.md:
- Add "API Specification" section (OpenAPI/Swagger documentation)
- Add "Endpoint Implementation" section (routes, middleware, validation)
- Add "Authentication & Authorization" section (OAuth, JWT, API keys)
- Add "Rate Limiting & Security" section
```

#### Mobile App
```markdown
Customize todo.md:
- Add "Platform-Specific Tasks" (iOS, Android, React Native, Flutter)
- Add "App Store Deployment" section (certificates, screenshots, descriptions)
- Add "Mobile-Specific Testing" (device compatibility, offline mode)
- Add "Push Notifications" section (if applicable)
```

#### Data Pipeline / ETL
```markdown
Customize todo.md:
- Add "Data Source Integration" section (connectors, APIs, databases)
- Add "Data Transformation" section (cleaning, validation, enrichment)
- Add "Pipeline Orchestration" section (Airflow, Prefect, Dagster)
- Add "Data Quality" section (validation, monitoring, alerting)
```

---

## Recommended Project Structure

This template is flexible and works with any project structure. Here are common patterns:

### Web Application
```
my-project/
├── README.md
├── todo.md
├── .gitignore
├── requirements.txt (or package.json, etc.)
│
├── src/                    # Source code
│   ├── frontend/           # Frontend code (if applicable)
│   ├── backend/            # Backend code
│   └── shared/             # Shared utilities
│
├── tests/                  # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docs/                   # Documentation
│   ├── api/                # API documentation
│   └── architecture/       # Architecture decisions
│
├── config/                 # Configuration files
│   ├── dev.env
│   ├── staging.env
│   └── prod.env
│
└── scripts/                # Automation scripts
    ├── deploy.sh
    └── seed-db.sh
```

### CLI Tool
```
my-cli/
├── README.md
├── todo.md
├── .gitignore
├── requirements.txt (or Cargo.toml, etc.)
│
├── src/                    # Source code
│   ├── commands/           # Command implementations
│   ├── utils/              # Utility functions
│   └── main.rs             # Entry point (language-specific)
│
├── tests/
│
├── docs/
│   └── commands/           # Command documentation
│
└── examples/               # Usage examples
```

### Library/Package
```
my-library/
├── README.md
├── todo.md
├── .gitignore
├── requirements.txt (or package.json, etc.)
│
├── src/                    # Source code
│   └── lib/                # Library code
│
├── tests/
│
├── docs/
│   └── api/                # API reference
│
├── examples/               # Usage examples
│
└── benchmarks/             # Performance benchmarks
```

**Adapt these structures to your specific needs.** The key is keeping your project organized so Claude can easily navigate and understand your codebase.

---

## Claude Code Tips & Tricks

### 🎯 Power Techniques

#### 1. **Periodic Alignment Checks**
```markdown
You: "Read todo.md and tell me what we should focus on next based on our current progress."

Claude: [Reviews completed tasks and suggests next priorities]
```

#### 2. **Automated Status Updates**
```markdown
You: "After each task you complete, automatically update todo.md with [x] and move [-] to the next task."
```

#### 3. **Progressive Feature Building**
```markdown
You: "Start implementing the User Authentication feature. Update the [%] completion marker after each sub-task:
- [% 0] Initial state
- [% 25] Registration endpoint done
- [% 50] Login endpoint done
- [% 75] Password reset done
- [% 100] All auth features complete"
```

#### 4. **Architecture Discussions**
```markdown
You: "I've marked several tasks with [@] in the Core Development section. Let's discuss each one and make decisions before implementing."

Claude: [Analyzes [@] tasks and provides recommendations for each]
```

#### 5. **Refactoring Sessions**
```markdown
You: "Find tasks marked with [~] in todo.md. These are on hold for refactoring. Let's tackle them one by one."
```

#### 6. **Bug Triage**
```markdown
You: "Check the Bug Tracking section. Prioritize bugs marked [⚠] critical and [!] high priority first."
```

### 🔄 Workflow Integration

#### Using `/commit` with todo.md
```bash
# After Claude completes a feature
You: "Update todo.md to mark tasks complete, then /commit with a message referencing the completed tasks."

Claude: [Updates todo.md, creates commit]
# Commit message: "Implement user registration endpoint (completes todo.md tasks 1-3)"
```

#### Memory & Context
```markdown
You: "Remember that we're building a REST API with JWT authentication, as outlined in todo.md's Project Setup section."

Claude: [Stores context for future sessions]
```

### 📊 Progress Tracking

#### Weekly Reviews
```markdown
You: "Review todo.md. How many tasks did we complete this week? What's our velocity?"

Claude: [Analyzes completed [x] tasks, provides summary]
```

#### Milestone Tracking
```markdown
You: "Check if all [!] high-priority tasks in the 'Core Development' section are complete. If so, we've hit our MVP milestone."
```

---

## Next Steps & Resources

### 🚀 Getting Started

1. **Customize this template** for your project's specific needs
2. **Fill out todo.md** with your initial project tasks
3. **Start your first Claude Code session** and share todo.md
4. **Begin with Project Setup** tasks marked [!] high priority

### 📚 Learning Resources

**Claude Code Documentation:**
- [Claude Code Official Docs](https://docs.anthropic.com/claude-code) - Official documentation and guides
- [Claude API Documentation](https://docs.anthropic.com/api) - For building custom integrations

**Best Practices:**
- [Effective Prompting for Code](https://docs.anthropic.com/prompts) - Write better prompts for Claude
- [Claude Code Workflows](https://support.anthropic.com/claude-code) - Common development workflows

**Community & Examples:**
- [Claude Code GitHub](https://github.com/anthropics/claude-code) - Official examples and templates
- [Community Templates](https://github.com/topics/claude-code-template) - User-contributed templates

### 🛠 Recommended Tools & Integrations

**IDE/Editor Extensions:**
- VS Code: Install Claude Code extension for seamless integration
- JetBrains IDEs: Claude Code plugin available
- Vim/Neovim: Command-line claude interface

**Development Tools:**
- **Version Control**: Git (already included in template)
- **CI/CD**: GitHub Actions, GitLab CI, CircleCI
- **Testing**: Framework-specific (Jest, pytest, cargo test, etc.)
- **Linting**: ESLint, Pylint, Clippy, etc.
- **Formatting**: Prettier, Black, rustfmt, etc.

**Project Management:**
- Use todo.md as your primary task tracker
- Optional: Sync with Linear, Jira, or GitHub Issues
- Track milestones and sprints alongside todo.md

### 💡 Pro Tips

1. **Keep todo.md updated** - It's your shared source of truth with Claude
2. **Use specific symbols** - Help Claude understand priority and status at a glance
3. **Break down large features** - Smaller tasks = better Claude Code sessions
4. **Reference file paths** - Help Claude navigate your codebase efficiently
5. **Review regularly** - Ask Claude to analyze todo.md and suggest improvements

---

## Contributing

Found ways to improve this template? Have suggestions for better Claude Code integration? Contributions are welcome!

**To contribute:**
1. Fork this repository
2. Make your improvements
3. Submit a pull request with a clear description

**Ideas for contributions:**
- Additional language-specific examples
- Project type variations (game dev, embedded systems, etc.)
- Claude Code workflow optimizations
- Better symbol system variations

---

## License

This template is provided as-is for anyone to use freely. Adapt it to your needs!

---

## Credits

Created for the developer community to accelerate project development with Claude Code.

**Template Version**: 3.0
**Last Updated**: 2026-02-12
**Maintained by**: wema.digital

---

## FAQ

**Q: Do I need Claude Code to use this template?**
A: No, the todo.md system works great standalone. But it's optimized for Claude Code workflows.

**Q: Can I use this for non-software projects?**
A: Absolutely! The task tracking system works for any project. Just customize todo.md sections.

**Q: What if my language isn't listed?**
A: The template is language-agnostic. Replace requirements.txt with your language's dependency file and adapt todo.md sections as needed.

**Q: How do I integrate this with my existing project?**
A: Copy `todo.md` and `README.md` into your existing project. Adapt the task sections to match your current progress.

**Q: Can I modify the symbol system?**
A: Yes! The symbol guide in todo.md is fully customizable. Add or remove symbols to match your workflow.

**Q: How do I share this template with my team?**
A: Fork or clone this repo, customize it for your team's stack and workflow, then share the link or use it as a template repository on GitHub.

---

**Ready to build something amazing? Start by customizing `todo.md` and let Claude Code help you bring your project to life! 🚀**
