> **Status**: Executed 2026-02-12. Reviewed and updated 2026-08-24 (dates bumped to v3.1, CLAUDE.md added). Superseded by root `claude/` planning documents for future changes.

Context
This project is meant to be a general-purpose, language-agnostic starter template that any new user can quickly use to start developing projects with Claude Code. Currently, the todo.md file is heavily focused on SQL database projects, which is too specific for a general template. The README is also minimal and doesn't provide guidance on how to use this template effectively with Claude Code.
Goals:

Transform todo.md from SQL-database-specific to a language-agnostic software development template
Enhance README.md with clear instructions on using this template with Claude Code-specific best practices
Keep the sophisticated symbol/status system from the current todo.md (it's excellent)
Handle requirements.txt appropriately for language-agnostic use

Current State

todo.md: Comprehensive SQL database project template with excellent symbol system for tracking task status
requirements.txt: Python-specific dependencies (pytest, python-dotenv, pandas)
README.md: Minimal (3 lines) - needs expansion
Project structure: Clean, git-based, currently Python-focused but needs to be language-agnostic

Implementation Plan
1. Update todo.md (Transform to Language-Agnostic Template)
Keep the same format structure:

Maintain the comprehensive symbol system ([ ], [x], [-], [~], [>], [!], [?], [@], [$], [#], [%], [→], [⚠])
Keep the metadata footer structure
Preserve the clean hierarchical organization
Include detailed examples showing how to use the symbols

Replace database-specific sections with language-agnostic software development phases:
New Section Structure:

Project Setup & Planning

Project initialization (version control, environment setup)
Requirements gathering and analysis
Architecture/design decisions
Technology stack selection
Dependency management setup
Development environment configuration
Example tasks with symbols to demonstrate usage


Core Development

Feature implementation tasks
Module/component development
API/interface design
UI/UX implementation (if applicable)
Business logic implementation
Example tasks showing priority markers and status


Code Quality & Documentation

Code review tasks
Technical documentation
API documentation
README and user guides
Code refactoring
Linting and formatting
Example tasks with delegation and discussion markers


Testing & Quality Assurance

Unit tests
Integration tests
End-to-end tests
Performance testing
Security testing
Test coverage goals
Bug tracking and fixes
Example tasks with percentage completion tracking


Deployment & DevOps

Build system setup
CI/CD pipeline configuration
Environment configuration (dev/staging/prod)
Deployment automation
Container/orchestration setup
Monitoring and logging
Example tasks with critical issue markers


Maintenance & Optimization

Performance profiling and optimization
Security updates and patches
Dependency updates
Technical debt reduction
Backward compatibility
Example tasks with research needs markers



Symbol System Section:

Comprehensive legend explaining all symbols
Usage examples for each symbol type
Composite symbol combinations
Guidelines for custom emoji additions
Notes on how Claude Code can help track these statuses

Update metadata footer:

Remove database-specific references (PostgreSQL/MySQL versions)
Add: Template version, last updated date, applicable to any language/framework
Include customization guidance

2. Update README.md (Comprehensive Claude Code Template Guide)
New README structure with Claude Code-specific guidance:

Title & Description

Clear explanation: "Claude Code Project Template - Quick Start for Any Language"
Target audience: developers new to Claude Code who want structured project development
Language-agnostic approach


Quick Start Guide

Clone/fork this template
Initialize your project (git, dependencies for your language)
Start working with Claude Code using todo.md as your task tracker
Recommended first steps


What's Included

todo.md: Comprehensive task tracking template with symbol system
README.md: This guide
.gitignore: Standard patterns
requirements.txt: Example Python dependencies (can be replaced with your language's equivalent)
Brief overview of the symbol system (point to todo.md for full details)


Working with Claude Code (MAJOR SECTION)

Task Breakdown Strategy: How to break large features into Claude-friendly chunks
Effective Prompting: How to reference todo.md tasks when prompting Claude
Iterative Development: Using Claude for incremental implementation following todo.md structure
Status Tracking: How to update todo.md as Claude completes tasks
Code Review with Claude: Using Claude to review completed work against requirements
Documentation Generation: Having Claude document code as it's written
Best Practices:

Keep tasks atomic and well-defined
Use specific symbol markers Claude can understand
Reference file paths in tasks
Ask Claude to update todo.md status after completing tasks




Symbol System Quick Reference

Brief table of common symbols and their meanings
Link to todo.md for complete documentation
Tips on which symbols to use with Claude (e.g., [!] for high priority, [@] when you need to discuss approach)


Customization Guide

For Different Languages:

Python: Keep requirements.txt
JavaScript/Node: Replace with package.json
Go: Replace with go.mod
Rust: Replace with Cargo.toml
Java: Replace with pom.xml or build.gradle


For Different Project Types:

Web applications
CLI tools
Libraries/packages
APIs/microservices
Data pipelines
Mobile apps


Adding project-specific sections to todo.md
Customizing symbol system for your team


Recommended Project Structure

Language-agnostic best practices
Common directory patterns (src, tests, docs, etc.)
Where to place configuration files
Documentation organization


Claude Code Tips & Tricks

Using /commit after completing todo.md sections
Asking Claude to read todo.md periodically to stay aligned
Having Claude suggest next tasks based on completed work
Using Claude for refactoring marked with [~] in todo.md
Leveraging Claude's memory for project context


Next Steps & Resources

Link to Claude Code documentation
Link to Claude AI best practices
Community templates and examples
Suggested IDE/editor integrations
Additional tooling recommendations



3. Update requirements.txt (Make it an Example)
Action: Rename or reposition requirements.txt as an example for Python projects
Options:
A. Rename to requirements.txt.example with a note in README
B. Keep as-is but add clear comments explaining it's Python-specific
C. Move to an examples/ directory with examples for other languages
Recommended: Option B - Keep the file as a working example, add header comments:
# Example Python project dependencies
# For other languages, replace this file:
# - Node.js: package.json
# - Go: go.mod
# - Rust: Cargo.toml
# - Java: pom.xml / build.gradle

pytest>=7.4.0
python-dotenv>=1.0.0
pandas>=2.0.0
This approach:

Provides immediate value for Python developers
Clearly indicates language-agnostic intent
Guides users on what to do for their language
Doesn't require deleting useful content

Critical Files to Modify

W:\vscode.workspaces\wema.digital.github\coding-project-templates\features\claude-code-basic\todo.md - Transform to language-agnostic template
W:\vscode.workspaces\wema.digital.github\coding-project-templates\features\claude-code-basic\README.md - Comprehensive guide with Claude Code best practices
W:\vscode.workspaces\wema.digital.github\coding-project-templates\features\claude-code-basic\requirements.txt - Add explanatory comments

Verification Steps
After implementation:

Read all three updated files to ensure formatting is preserved
Verify the symbol system in todo.md is intact with clear, detailed examples
Check that README provides comprehensive Claude Code-specific guidance
Ensure the template is truly language-agnostic (no language favoritism)
Confirm todo.md examples are applicable across different project types
Verify README explains how to adapt the template for different languages
Check that Claude Code best practices section is actionable and specific
Ensure requirements.txt comments clarify its example nature

Design Decisions
Why make the template language-agnostic:
User explicitly chose language-agnostic approach. This makes the template useful for JavaScript, Go, Rust, Java, Python, and any other language developers might use. The core task management concepts apply universally.
Why keep the symbol system with detailed examples:
The current todo.md has an excellent, comprehensive status tracking system. User chose "detailed with examples" to help new users understand how to use the symbols effectively. Examples make the template immediately actionable.
Why focus heavily on Claude Code best practices:
User explicitly requested Claude-specific guidance. This is the template's key differentiator - it's not just a generic project template, it's optimized for development workflows using Claude Code. The README should teach users how to work effectively with Claude.
Why keep detailed examples in todo.md:
Users learn best from examples. Showing actual task entries with different symbols demonstrates the system better than just explaining it abstractly. Examples should span multiple project types to maintain language-agnostic nature.
Why add comments to requirements.txt instead of deleting:
Provides immediate value for Python users while clearly indicating how to adapt for other languages. Deleting would leave nothing; keeping as an example is more helpful.
Why structure README with major "Working with Claude Code" section:
This is the core value proposition. New Claude Code users need specific, actionable guidance on how to integrate Claude into their development workflow, not just generic project setup instructions.