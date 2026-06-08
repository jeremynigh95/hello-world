"""GUI layer (PySide6/Qt). The thin outer shell.

Imports from ``core`` and ``db`` only. Contains *no* business rules:
character counts, colors, and suggestion ranking are all delegated to
``core``; data access is delegated to a ``PhraseRepository``. If you find
yourself writing an ``if`` about lengths or colors here, it belongs in core.
"""
