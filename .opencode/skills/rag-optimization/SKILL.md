---
name: rag-optimization
description: Enhances Retrieval-Augmented Generation pipelines for speed and accuracy.
license: MIT
compatibility: opencode
---

# RAG Optimization

## Purpose
Enable agents to maximize the effectiveness of RAG pipelines in retrieving relevant knowledge.

## When to Use This Skill
Use this skill when an existing RAG pipeline has poor retrieval accuracy, high latency, or irrelevant context in responses.


## Rules
1. Always validate retrieval outputs for correctness.
2. Avoid unnecessary data duplication in indexes.
3. Document pipeline configuration and tuning decisions.

## Output Format
Provide:
- Current pipeline performance baseline (latency, relevance scores)
- Optimization changes applied with expected impact
- A/B test or benchmark comparison results
- Updated pipeline configuration
