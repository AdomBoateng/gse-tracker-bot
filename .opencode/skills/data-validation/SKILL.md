---
name: data-validation
description: Validates data to ensure accuracy, consistency, and reliability for analytics and ML pipelines.
license: MIT
compatibility: opencode
---

# Data Validation

## Purpose
Enable agents to automatically check data quality, integrity, and adherence to expected formats before it is used in production pipelines or machine learning models.

## When to Use This Skill
Use this skill when verifying data quality before it enters a production pipeline, ML model, or analytics system.


## Rules
1. Always back up original datasets before performing validation.
2. Log all validation results, including errors and warnings.
3. Ensure that only validated, clean data is passed to downstream pipelines or models.
4. Integrate with data-cleaning processes to automatically correct minor issues when appropriate.
5. Use reusable validation scripts and standard rules for consistency across projects.

## Output Format
Provide:
- Validation rules applied per field or dataset
- Validation report (pass/fail counts, error samples)
- Recommended fixes for failed validations
- Script or configuration used for validation
