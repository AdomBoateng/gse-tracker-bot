---
name: vector-database-tuning
description: Tunes vector databases for fast, accurate, and scalable searches.
license: MIT
compatibility: opencode
---

# Vector Database Tuning

## Purpose
Enable agents to configure vector databases for optimal similarity search and embedding management.

## When to Use This Skill
Use this skill when a vector search index is too slow, returning poor results, or needs to scale to a larger dataset.


## Rules
1. Always validate search results for accuracy.
2. Avoid overloading indexes with unnecessary vectors.
3. Document all tuning parameters and performance metrics.

## Output Format
Provide:
- Current index configuration and baseline performance metrics
- Tuning changes applied (index type, distance metric, HNSW params, etc.)
- Before/after query latency and recall benchmarks
- Recommended production configuration
