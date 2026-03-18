---
name: llm-guardrails
description: Implements safety and instruction compliance for language models.
license: MIT
compatibility: opencode
---

# LLM Guardrails

## Purpose
Enable agents to control LLM outputs, preventing hallucinations, unsafe content, or off-topic responses.

## When to Use This Skill
Use this skill when enforcing safety, compliance, or task-specific constraints on LLM inputs or outputs.


## Rules
1. Never bypass safety constraints.
2. Keep guardrails modular and reusable across tasks.
3. Document guardrail logic and thresholds for maintainability.

## Output Format
Provide:
- Guardrail rules defined (input filters, output filters)
- Trigger conditions and rejection messages
- Audit log format
- Test cases validating guardrail behavior
