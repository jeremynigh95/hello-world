# ADR-002: pytest as Test Framework

**Date:** 2026-06-07
**Status:** Accepted

## Context
Needed a test framework for verifying correctness and preventing regressions as the project grows.

## Decision
Use pytest with pytest-cov for all testing. Enforce 80% minimum coverage on source code.

## Reasons
- Industry standard for Python projects
- Simple syntax — plain `assert` statements, no boilerplate classes
- Rich plugin ecosystem (cov, mock, parametrize, etc.)
- Excellent IDE and CI integration

## Alternatives Considered
| Option | Why rejected |
|---|---|
| unittest (stdlib) | More boilerplate; pytest is strictly superior for new projects |
| nose2 | Largely superseded by pytest |

## Consequences
- `pytest` and `pytest-cov` must be installed in dev environments (`pip install pytest pytest-cov`)
- All tests live under `tests/`, mirroring source structure
- CI enforces the full suite on every push via GitHub Actions
- Coverage below 80% fails the build
