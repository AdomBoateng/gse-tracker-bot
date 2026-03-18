---
name: data-cleaning
description: Cleans and preprocesses raw data for analysis or ML pipelines.
license: MIT
compatibility: opencode
---

# Data Cleaning

## Purpose
Enable agents to prepare datasets by removing errors, inconsistencies, and duplicates to ensure high-quality inputs.

## When to Use This Skill
Use this skill when raw datasets contain missing values, duplicates, formatting inconsistencies, or anomalies.


## Rules
1. Always back up original datasets before cleaning.
2. Log all changes for reproducibility.
3. Follow project-specific data standards and formats.

## Output Format
Provide:
- Summary of identified data issues (nulls, duplicates, anomalies)
- Cleaning transformations applied with justification
- Before/after data quality metrics
- Cleaned dataset file path or schema
