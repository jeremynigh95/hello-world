# Architecture

## Overview

_High-level description of what this system does and why it exists._

## Component Map

```
┌─────────────────────────────────────────┐
│                  hello-world            │
│                                         │
│  ┌─────────────┐     ┌───────────────┐  │
│  │   CLI / UI  │────▶│  Core Logic   │  │
│  └─────────────┘     └───────┬───────┘  │
│                              │          │
│                      ┌───────▼───────┐  │
│                      │  Data Layer   │  │
│                      └───────────────┘  │
└─────────────────────────────────────────┘
```

_Replace with your actual components as the project grows._

## Layers

### CLI / UI
Entry point for the user. Responsible for parsing input and displaying output. No business logic here.

### Core Logic
The heart of the application. All business rules live here. Should have no knowledge of how it's invoked or where data is stored.

### Data Layer
Handles persistence (files, database, API calls, etc.). Core logic calls into this layer; it never calls back up.

## Key Design Principles
- Layers only depend downward (UI → Core → Data)
- Core logic is pure and independently testable
- No business logic in the CLI or data layer

## External Dependencies
| Dependency | Purpose | Decision |
|---|---|---|
| Python 3.12 | Runtime | [ADR-001](decisions/001-python-as-primary-language.md) |

## Data Flow
_Describe how data moves through the system for the primary use case._

1. User invokes CLI
2. CLI delegates to Core Logic
3. Core Logic reads/writes via Data Layer
4. Result returned up the chain and displayed

## Future Considerations
- _Note architectural concerns or planned evolution here_
