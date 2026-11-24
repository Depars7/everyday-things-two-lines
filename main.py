"""Everyday Things, Two Lines, Longer Run — entry writer.

Writes a two-line explanation of a vacuum cleaner for a 10-year-old to
/output/entry.txt:

- Line 1: one vivid sentence built on a single analogy (a tame elephant
  on wheels whose trunk sucks up crumbs and dust into its tummy).
- Line 2: one sentence saying why the analogy works — what it maps
  (hose/trunk sucking, bin/tummy holding) and what it leaves out
  (the motor and fan that actually do the sucking).

The file is written as exact UTF-8 bytes: a single newline between the
two lines and no trailing newline. The gate (UTF-8 text, 1-400
characters, not only whitespace, exactly two lines) is validated with
assertions before anything is written.
"""

import os

LINE_1 = (
    "A vacuum cleaner is a tame elephant on wheels, sucking crumbs and "
    "dust up its long trunk nose and holding them in its tummy."
)
LINE_2 = (
    "That fits because the hose sucks like a trunk and the bin holds "
    "dirt like a tummy, but it leaves out the motor and fan that do "
    "the sucking, since an elephant uses muscles."
)

ENTRY_TEXT = LINE_1 + "\n" + LINE_2
OUTPUT_PATH = "/output/entry.txt"


def validate(text: str) -> bytes:
    """Check the sealed gate and return the exact bytes to write."""
    data = text.encode("utf-8")
    # Gate: valid UTF-8 (round-trips), 1-400 characters, not whitespace only.
    assert data.decode("utf-8") == text
    assert 1 <= len(text) <= 400, f"character count out of gate: {len(text)}"
    assert text.strip(), "entry must not be only whitespace"
    # Format: exactly two lines, each a single non-empty sentence.
    lines = text.split("\n")
    assert len(lines) == 2, f"entry must have exactly two lines: {len(lines)}"
    for line in lines:
        assert line and line == line.strip(), "line is empty or padded"
        assert line.endswith("."), "each line is one sentence ending in '.'"
        assert line.count(".") == 1, "each line must be a single sentence"
    assert not text.endswith("\n"), "no trailing newline allowed"
    return data


def write_entry(data: bytes) -> None:
    """Write the validated bytes and leave the file readable by all."""
    parent = os.path.dirname(OUTPUT_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    # The collector reads the output as another user: make the file
    # readable by everyone. Only the file is chmodded, never /output.
    os.chmod(OUTPUT_PATH, 0o644)


def verify_written(expected: bytes) -> None:
    """Fail loudly if the file on disk is not exactly what was validated."""
    with open(OUTPUT_PATH, "rb") as handle:
        on_disk = handle.read()
    assert on_disk == expected, "written bytes differ from validated bytes"
    mode = os.stat(OUTPUT_PATH).st_mode & 0o777
    assert mode == 0o644, f"unexpected output file mode: {oct(mode)}"


def main() -> None:
    os.umask(0o022)
    data = validate(ENTRY_TEXT)
    write_entry(data)
    verify_written(data)


if __name__ == "__main__":
    main()
