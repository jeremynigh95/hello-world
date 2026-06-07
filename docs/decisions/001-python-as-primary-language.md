# ADR-001: Python as Primary Language

**Date:** 2026-06-07
**Status:** Accepted

## Context
Needed to choose a primary language for this project. Key requirements were: quick to iterate, readable, strong standard library, wide ecosystem.

## Decision
Use Python 3.12 as the sole implementation language.

## Reasons
- Minimal boilerplate — fast to prototype and iterate
- Large ecosystem (pytest, requests, etc.) covers most needs without custom tooling
- Strong Claude Code support for Python projects
- Low barrier to entry for future contributors

## Alternatives Considered
| Option | Why rejected |
|---|---|
| JavaScript/Node | Better suited for web-first projects; this is CLI-focused |
| Go | Stronger for compiled binaries/services; overhead not justified here |
| Bash | Not suitable for anything beyond simple scripting |

## Consequences
- All contributors need a Python 3.12+ environment
- Packaging/distribution handled via pip / pyproject.toml when needed
- Type hints encouraged but not enforced
