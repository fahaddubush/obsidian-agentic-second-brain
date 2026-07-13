from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".css", ".json", ".md", ".py", ".svg", ".toml", ".yaml", ".yml"}
SKIP_PREFIXES = (
    (".git",),
    (".codex", "state"),
    (".obsidian", "plugins"),
    (".obsidian", "themes"),
    ("07_Sources",),
)
FORBIDDEN_DASHES = {"\u2013", "\u2014"}
EMOJI_RANGES = (
    (0x2600, 0x27BF),
    (0x1F000, 0x1FAFF),
)


def generated_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.casefold() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(ROOT)
        if "__pycache__" in relative.parts:
            continue
        if any(relative.parts[: len(prefix)] == prefix for prefix in SKIP_PREFIXES):
            continue
        files.append(path)
    return files


def emoji_characters(text: str) -> set[str]:
    return {
        character
        for character in text
        if any(start <= ord(character) <= end for start, end in EMOJI_RANGES)
    }


class PublicStyleTest(unittest.TestCase):
    def test_generated_text_has_no_long_dashes_or_emoji(self) -> None:
        findings: list[str] = []
        for path in generated_text_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            dashes = sorted(FORBIDDEN_DASHES.intersection(text))
            emoji = sorted(emoji_characters(text))
            if dashes or emoji:
                findings.append(
                    f"{path.relative_to(ROOT)}: long_dashes={len(dashes)}, emoji={len(emoji)}"
                )
        self.assertEqual(findings, [], "Public generated text style violations:\n" + "\n".join(findings))


if __name__ == "__main__":
    unittest.main()
