---
name: containerization
description: Creates and manages containerized services.
license: MIT
compatibility: opencode
---

# Containerization

## Purpose
Enable agents to package services for reproducible and scalable deployments.

## When to Use This Skill
Use this skill when packaging a service into Docker, creating Compose setups, or managing Kubernetes deployments.


## Rules
1. Avoid unnecessary dependencies in containers.
2. Keep images modular for reusability.
3. Document container specifications.

## Output Format
Provide:
- Dockerfile and/or Docker Compose configuration
- Image size and layer breakdown notes
- Environment variable and secrets handling instructions
- Commands to build, run, and verify the container
