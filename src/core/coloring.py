"""Map a string's length to a display color.

The rule: every 10 characters bumps to the next color band.
  1-10   -> black
  11-20  -> dark blue
  21-30  -> dark green
  31-40  -> dark red
  41-50  -> indigo
  51-60  -> saddle brown
  61+    -> clamped to the last band

Colors are returned as hex strings so this layer stays GUI-agnostic.
The GUI decides how to apply them (stylesheet, item foreground, etc.).
"""

# Indexed by 10-character band. Band 0 covers lengths 0-10.
PALETTE = [
    "#000000",  # black
    "#00008B",  # dark blue
    "#006400",  # dark green
    "#8B0000",  # dark red
    "#4B0082",  # indigo
    "#8B4513",  # saddle brown
]


def color_for_length(length: int) -> str:
    """Return the hex color for a string of ``length`` characters.

    Raises ``ValueError`` for negative lengths. Lengths beyond the last
    band clamp to the final color rather than cycling.
    """
    if length < 0:
        raise ValueError("length must be non-negative")
    band = max(0, (length - 1) // 10)
    band = min(band, len(PALETTE) - 1)
    return PALETTE[band]
