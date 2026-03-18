---
name: hallucination-detection
description: Detects AI-generated outputs that are inaccurate or fabricated.
license: MIT
compatibility: opencode
---

# Hallucination Detection

## Purpose
Enable agents to ensure factual correctness and prevent false information.

## When to Use This Skill
Use this skill when verifying AI-generated outputs for factual accuracy before they are used or shown to users.


## Rules
1. Always provide sources or confidence scores.
2. Avoid passing unverified information to end-users.
3. Integrate with memory and RAG pipelines for fact-checking.

## Output Format
Provide:
- List of flagged statements with confidence scores
- Source references supporting or contradicting each claim
- Overall hallucination risk rating (low / medium / high)
- Recommended corrections or caveats
