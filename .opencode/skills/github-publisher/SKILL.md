---
name: github-publisher
description: Publishes a local project to GitHub for the first time by creating a repository, generating a professional README, writing structured documentation, composing a conventional commit message, and pushing all files via the GitHub MCP server.
license: MIT
compatibility: opencode
---

# GitHub Publisher

## Purpose
Enable agents to take any local project from zero to a fully published GitHub repository with professional documentation, a clean commit history, and an informative README — all in a single automated workflow.

## When to Use This Skill
Use this skill when a user wants to publish a local project to GitHub for the first time, has no existing remote repository, and needs the repository created, documented, and pushed automatically.

## Prerequisites
Before invoking this skill, confirm:
- The GitHub MCP server is configured in `opencode.json` with a valid `GITHUB_PERSONAL_ACCESS_TOKEN`
- The token has `repo` and `workflow` scopes
- The user has confirmed whether the repository should be public or private

## Workflow

### 1. Analyse the project
- Read all project files to understand purpose, tech stack, and structure
- Identify primary language, frameworks, entry points, and dependencies
- Note any existing README, license, or documentation to preserve or improve

### 2. Generate README.md
Produce a professional README.md containing:
- Project title and one-line description
- Badges (language, license, version if applicable)
- Overview of what the project does and why it exists
- Tech stack and architecture summary
- Prerequisites and installation steps
- How to run, configure, and use the project
- Folder structure with brief role descriptions
- Environment variables or configuration reference
- Contributing guidelines pointer
- License statement

### 3. Generate supporting documentation
Create the following under `.opencode/docs/`:
- `ARCHITECTURE.md` — system components, data flow, design decisions
- `CONTRIBUTING.md` — branch naming convention, commit format, PR process, code style
- `CHANGELOG.md` — initial entry for v0.1.0 with today's date and a summary of what is included

### 4. Compose the commit message
Follow the Conventional Commits specification: