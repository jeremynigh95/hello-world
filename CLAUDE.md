# hello-world

A Python project used as a learning sandbox for Claude Code + Python development workflows.

## Stack
- Language: Python 3.12
- Runner: `python hello.py`

## How to run
```bash
python hello.py
```

## How to test
No test suite yet. When added, run with:
```bash
python -m pytest
```

## Project structure
```
hello-world/
├── hello.py          # main program
├── CLAUDE.md         # this file — always read at session start
├── README.md         # public-facing docs
└── .claude/
    ├── PLAN.md       # milestones and task checklist
    └── STATUS.md     # current state snapshot — update before ending a session
```

## Session startup checklist
When starting a new session, read these files in order:
1. `CLAUDE.md` (this file)
2. `.claude/PLAN.md`
3. `.claude/STATUS.md`
4. `git log --oneline -10`

## Conventions
- Commit after each meaningful unit of work
- Update `.claude/STATUS.md` before ending a session
- Check off completed items in `.claude/PLAN.md` as work finishes
