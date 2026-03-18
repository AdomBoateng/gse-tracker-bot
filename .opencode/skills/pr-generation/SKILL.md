---
name: pr-generation
description: Automates pull request creation with proper titles and descriptions.
license: MIT
compatibility: opencode
---

# Pull Request Generation

## Purpose
Enable agents to create consistent, informative, and review-ready PRs.

## When to Use This Skill
Use this skill when generating a pull request description, changelog entry, or commit summary for completed work.


## Rules
1. Ensure PRs are concise and relevant.
2. Avoid including unrelated changes.
3. Follow repository branch policies.

## Output Format
Provide:
- PR title following conventional commit format
- PR description with: summary, motivation, changes made, testing notes
- Labels, reviewers, and linked issues
- Checklist of pre-merge requirements
