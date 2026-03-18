---
name: orchestrator
description: Coordinates workflows and manages multiple agents efficiently.
license: MIT
compatibility: opencode
---

# Orchestrator

## Purpose
Enable agents to plan, delegate, and monitor tasks across the project’s agent network.

## When to Use This Skill
Use this skill when coordinating a multi-agent workflow, breaking down a complex goal, or tracking cross-agent task dependencies.


## Rules
1. Always verify that each subtask has an assigned agent.
2. Avoid overloading agents with multiple high-complexity tasks at once.
3. Maintain a global view of project dependencies and timelines.

## Output Format
Provide:
- Task breakdown with assigned agents and dependencies
- Execution order and estimated completion steps
- Status tracking format (pending / in-progress / done / blocked)
- Escalation path for unresolved blockers
